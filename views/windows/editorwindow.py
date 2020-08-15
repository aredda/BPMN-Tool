from tkinter import *
from PIL import Image as Img, ImageTk as ImgTk, ImageGrab as ImgGrb
from datetime import datetime
from threading import Thread
from time import sleep
from math import sqrt, pow
from io import BytesIO
import canvasvg as cnvsvg
import pickle as pk
from resources.colors import *
from helpers.stringhelper import to_pretty_xml
from helpers.deserializer import Deserializer
from helpers.xmlutility import elementtobytes, bytestoelement
from helpers.filehelper import filetobytes
from models.bpmn.definitions import Definitions
from models.bpmn.lane import Lane
from models.bpmn.sequenceflow import SequenceFlow
from models.bpmn.messageflow import MessageFlow
from models.bpmn.dataassociation import DataAssociation, DataAssocDirection
from models.entities.Entities import Project, Session, Collaboration, ShareLink, History
from models.entities.Container import Container
from models.bpmndi.diagram import BPMNDiagram
from models.bpmndi.plane import BPMNPlane
from views.windows.abstract.sessionwindow import SessionWindow
from views.components.scrollable import Scrollable
from views.components.listitem import ListItem
from views.components.icon import IconFrame
from views.components.textbox import TextBox
from views.factories.iconbuttonfactory import *
from views.prefabs.abstract.guicontainer import GUIContainer
from views.prefabs.abstract.guilinkable import GUILinkable
from views.prefabs.guievent import GUIEvent
from views.prefabs.guigateway import GUIGateway
from views.prefabs.guisubprocess import GUISubProcess
from views.prefabs.guitask import GUITask
from views.prefabs.guiprocess import GUIProcess
from views.prefabs.guidatastore import GUIDataStore
from views.prefabs.guidataobject import GUIDataObject
from views.prefabs.guiflow import GUIFlow
from views.prefabs.guilane import GUILane
from views.windows.modals.messagemodal import MessageModal

# this class represents the checkpoint made each time an action is done
# in order for the user to be able to cancel or redo actions
class Memento:
    def __init__(self, **args):
        for key in args.keys():
            setattr(self, key, args.get(key))

class EditorWindow(SessionWindow):
    
    toolSettings = {
        LEFT: {
            'size': 35,
            'path': 'resources/icons/ui/',
            'tools': [
                { 'icon': 'save.png', 'cmnd': 'save_work' },
                { 'icon': 'open.png', 'bg': danger, 'cmnd': 'back_to_subject' },
                { 'name': 'btn_delete_selected', 'icon': 'delete.png', 'bg': danger, 'cmnd': 'btn_delete_selected_click' }
            ]
        },
        RIGHT: {
            'size': 40,
            'path': 'resources/icons/notation/',
            'bg': white,
            'hoverBg': gray2,
            'tools': [
                { 'icon': 'startevent.png', 'create': GUIEvent },
                { 'icon': 'gateway.png', 'create': GUIGateway },
                { 'icon': 'task.png', 'create': GUITask },
                { 'icon': 'subprocess-expanded.png', 'create': GUISubProcess },
                { 'icon': 'participant.png', 'create': GUIProcess },
                { 'icon': 'data-object.png', 'create': GUIDataObject },
                { 'icon': 'data-store.png', 'create': GUIDataStore }
            ]
        },
        BOTTOM: {
            'size': 35,
            'path': 'resources/icons/ui/',
            'align': LEFT,
            'hoverBg': teal,
            'tools': [
                { 'icon': 'redo.png', 'cmnd': 'redo' },
                { 'icon': 'undo.png', 'cmnd': 'undo' },
                { 'name': 'btn_move_mode', 'icon': 'move.png', 'cmnd': 'enable_move_mode' },
                { 'name': 'btn_select_mode', 'icon': 'select.png', 'cmnd': 'enable_select_mode' },
                { 'icon': 'zoom_in.png', 'cmnd': 'zoom_in' },
                { 'icon': 'zoom_out.png', 'cmnd': 'zoom_out' }
            ]
        }
    }

    ACTION_HIST = {
        'undo': [],
        'redo': []
    }

    # command & event config method
    def select_event(self, tag, value):
        # create event
        if tag == 'create':
            # prepare create command
            def cmnd_create(e):
                # save undo checkpoint
                self.save_checkpoint(EditorWindow.ACTION_HIST['undo'])
                # instantiate
                guie = value(canvas=self.cnv_canvas)
                # draw
                guie.draw_at(0, 0)
                # show help information
                self.show_help_panel('Hover over the position you want to instantiate on, then left-click to drop; Press <Escape> if you want to cancel.')
                # change mode
                self.set_mode(self.CREATE_MODE)
                # set as the drag element
                self.DRAG_ELEMENT = guie
                # append
                # major collection
                self.guielements.append(guie)
                # definitions container
                if isinstance(guie, GUIProcess):
                    self.definitions.add(guie.element.get_tag(), guie.element)
                # di diagram container
                self.diplane.add('dielement', guie.dielement)
            # return it
            return cmnd_create
        # command event
        elif tag == 'cmnd':
            return lambda e: (getattr(self, value))()

    # EDITOR Modes
    DRAG_MODE = 0
    SELECT_MODE = 1
    MOVE_MODE = 2
    CREATE_MODE = 3
    LINK_MODE = 4
    RESIZE_MODE = 5

    def __init__(self, root, subject=None, **args):
        SessionWindow.__init__(self, root, **args)

        # data related attributes
        self.subject = subject
        self.guielements = []
        self.definitions: Definitions = Definitions()
        self.didiagram: BPMNDiagram = BPMNDiagram()
        self.diplane: BPMNPlane = BPMNPlane()

        # editor's gears
        self.SELECTED_MODE = self.DRAG_MODE
        self.SELECTED_ELEMENT = None
        self.SELECTED_ELEMENTS = []
        self.DRAG_ELEMENT = None
        self.IS_DRAGGING = False
        self.ZOOM_SCALE = 6
        self.MOVE_SCALE = [0, 0]

        # slight preparations
        self.design()
        self.setup_actions()

        self.definitions.add('diagram', self.didiagram)
        self.didiagram.add('plane', self.diplane)

        # draw func test
        if subject != None:
            # retrieve file
            f = subject.file if isinstance(subject, Project) else subject.project.file
            # check if there's a valid file
            if f != None:
                self.draw_diagram(f)
            else:
                self.create_default_process()
        else:
            self.create_default_process()
    
    def create_default_process(self):
        self.cnv_canvas.update()
        # instantiate a gui process
        guiprocess = GUIProcess(canvas=self.cnv_canvas)
        guiprocess.draw_at(int(self.cnv_canvas.winfo_width() / 2) - guiprocess.WIDTH / 2, int(self.cnv_canvas.winfo_height() / 2) - guiprocess.HEIGHT / 2)
        # adjustments
        guiprocess.dielement.element = guiprocess.element
        # append it
        self.guielements.append(guiprocess)    
        self.definitions.add('process', guiprocess.element)
        self.diplane.add('dielement', guiprocess.dielement)

    def setup_tools(self):
        # prepare an empty collection
        self.frm_tool_containers = []
        # Lay out tool panels
        for i in EditorWindow.toolSettings.keys():
            # get the settings of this set of tools
            settings = EditorWindow.toolSettings[i]
            # prepare a container
            pack_settings = { 'side': i, 'padx':20, 'pady':20 }
            frm_container = Frame(self.cnv_canvas, bg=white, highlightthickness=1, highlightbackground=border, padx=10, pady=10)
            frm_container.pack(**pack_settings)
            # save the container
            self.frm_tool_containers.append([frm_container, pack_settings])
            # for each action
            for j in settings['tools']:
                # adjust some configs
                align = settings.get('align', TOP)
                spacing = { 'padx': 0 if align == TOP else (0, 5), 'pady': 0 if align != TOP else (0, 5) }
                # command getter
                def get_cmnd(tag, value):
                    return self.select_event(tag, value)
                # process command
                cmnd = None
                for t in ['create', 'do', 'cmnd']:
                    if t in j: 
                        cmnd = get_cmnd(t, j.get(t))
                # instantiate button
                ic_tool = IconFrame(frm_container, settings['path'] + j.get('icon'), 15, j.get('bg', settings.get('bg', black)), settings['size'], cmnd, settings.get('hoverBg', None), bg=white)
                ic_tool.pack(side=align) 
                # if this button has a name, save it
                if 'name' in j:
                    setattr(self, j['name'], ic_tool)
                # add spacing to items
                if settings['tools'].index(j) != len(settings['tools']) - 1:
                    ic_tool.pack(side=align, **spacing)
        # create a help panel
        self.frm_help = Frame(self.cnv_canvas, bg=white, highlightthickness=1, highlightbackground=border, padx=10, pady=10)
        self.frm_help.pack(side=TOP, padx=20, pady=20)
        self.lbl_help = Label(self.frm_help, text='Help Label', bg=white, fg=black, font='-weight bold -size 9')
        self.lbl_help.pack()
        # hide help panel
        self.hide_help_panel()
        # deactivate delete selected button
        self.btn_delete_selected.pack_forget()
    
    def design(self):
        # prepare canvas
        self.frm_body.config(padx=0, pady=0)
        self.cnv_canvas = Canvas(self.frm_body, bg=background, highlightthickness=0, scrollregion=(0, 0, 2000, 2000))
        self.cnv_canvas.pack(fill=BOTH, expand=1)
        # prepare control frames
        self.setup_tools()

    def select_element(self, x, y):
        # retrieve the last element (top element) to be found in the canvas
        last_element = self.cnv_canvas.find_overlapping(x - 2, y - 2, x + 2, y + 2)
        if len (last_element) > 0: 
            last_element = last_element[-1]
        # return 
        return last_element

    def set_mode(self, mode):
        self.SELECTED_MODE = mode
        # reset view
        if mode == self.CREATE_MODE:
            self.reset_view()
        # change cursor
        if mode in [self.CREATE_MODE, self.MOVE_MODE]:
            self.cnv_canvas.config(cursor='hand2')
        elif mode in [self.RESIZE_MODE]:
            # save check point
            self.save_checkpoint(EditorWindow.ACTION_HIST['undo'])
            # reassign canvas
            self.assign_canvas_all()
            # change cursor
            self.cnv_canvas.config(cursor='size_ne_sw')
            # help panel
            self.show_help_panel('Left-click in order to cancel resize mode')
        else:
            self.cnv_canvas.config(cursor='')
        # if there are selected elements, deselect them
        if len (self.SELECTED_ELEMENTS) > 0:
            # deselect all
            for s in self.SELECTED_ELEMENTS: s.deselect()
            # clear
            self.SELECTED_ELEMENTS.clear()
        # deactivate delete button
        if mode != self.SELECT_MODE:
            # hide button
            self.btn_delete_selected.pack_forget()
            # disable effect
            self.btn_select_mode.defaultBgColor = black
            self.btn_select_mode.set_bgColor(black)
        # show link mode help info
        if mode == self.LINK_MODE:
            self.show_help_panel('Select an element in order to make a connection; Press <Escape> to cancel')            
        # move mode
        if mode != self.MOVE_MODE:
            # disable effect
            self.btn_move_mode.defaultBgColor = black
            self.btn_move_mode.set_bgColor(black)
        # default mode
        if mode == self.DRAG_MODE:
            self.hide_help_panel()

    # activating select mode
    def enable_select_mode(self):
        # change mode
        self.set_mode(self.SELECT_MODE)
        # activate delete button
        self.btn_delete_selected.pack(side=TOP)
        # activate effect
        self.btn_select_mode.defaultBgColor = teal
        # show information
        self.show_help_panel('Selection mode is enabled')

    # activating move mode
    def enable_move_mode(self):
        # change mode
        self.set_mode(self.MOVE_MODE)
        # activate effect
        self.btn_move_mode.defaultBgColor = teal
        # show information
        self.show_help_panel('Move mode is enabled, press arrows to move around the canvas')

    # responsible for refreshing all gui elements
    def reset(self):
        # clear all
        self.clear()
        # assign canvas
        self.assign_canvas_all()
        # redraw elements
        for e in self.guielements:
            # proceed to refresh
            e.erase()
            e.draw()

    # takes care of clearing
    def clear(self):
        self.cnv_canvas.delete('all')    

    # update view
    def update_view(self):
        self.cnv_canvas.xview_moveto(self.MOVE_SCALE[0])
        self.cnv_canvas.yview_moveto(self.MOVE_SCALE[1])
    
    # reset view
    def reset_view(self):
        self.MOVE_SCALE = [0, 0]
        self.update_view()

    # hide setup tools
    def hide_tools(self):
        for container in self.frm_tool_containers:
            container[0].pack_forget()

    # show tools
    def show_tools(self):
        for container in self.frm_tool_containers:
            container[0].pack(**container[1])   
        
    # pretty much the most important member of this module
    def setup_actions(self):
        
        # single click
        def action_mouse_click(e):
            # finish creation
            justCreated = False
            if self.SELECTED_MODE == self.CREATE_MODE:
                # reset mode
                self.set_mode(self.DRAG_MODE)
                # mark as 'just created'
                justCreated = True
                # hide the help panel
                self.hide_help_panel()
            # finish resizing
            if self.SELECTED_MODE == self.RESIZE_MODE:
                self.set_mode(self.DRAG_MODE)
                self.hide_help_panel()
            # hide components
            self.hide_component('frm_menu')
            self.hide_component('txt_input')
            # save the previous selected element
            previous_selected = self.SELECTED_ELEMENT
            # find gui element that has this element id
            self.SELECTED_ELEMENT = self.DRAG_ELEMENT = self.find_element(self.select_element(e.x, e.y))
            # BOOKMARK: LINK Functionality
            if self.SELECTED_ELEMENT != None and justCreated == False:
                # assign this element a canvas
                if self.SELECTED_ELEMENT.canvas == None:
                    self.assign_canvas(self.SELECTED_ELEMENT)
                # if select mode is enabled
                if self.SELECTED_MODE == self.SELECT_MODE:
                    # cases when some elements can't be selected
                    if isinstance(self.SELECTED_ELEMENT, GUIProcess):
                        self.show_help_panel('Process elements cannot be selected', danger)
                        return
                    # proceed normally
                    if self.SELECTED_ELEMENT in self.SELECTED_ELEMENTS:
                        self.SELECTED_ELEMENT.deselect()
                        self.SELECTED_ELEMENTS.remove(self.SELECTED_ELEMENT)
                    else:
                        self.SELECTED_ELEMENT.select()
                        self.SELECTED_ELEMENTS.append(self.SELECTED_ELEMENT)
                # if an element is selected
                if self.SELECTED_MODE == self.LINK_MODE:
                    if self.SELECTED_ELEMENT != previous_selected:
                        # check if we can link
                        if self.can_link(previous_selected, self.SELECTED_ELEMENT) == True:
                            # save undo checkpoint
                            self.save_checkpoint(EditorWindow.ACTION_HIST['undo'])
                            # emphasize that all elements have canvas
                            self.assign_canvas_all()
                            # generating a flow model
                            flowmodel = self.get_link_model(previous_selected, self.SELECTED_ELEMENT)
                            # creating a flow
                            flow = GUIFlow(canvas=self.cnv_canvas, guisource=previous_selected, guitarget=self.SELECTED_ELEMENT, element=flowmodel)
                            flow.draw_at(0, 0)
                            # if this model is a message flow
                            if isinstance(flowmodel, MessageFlow) == True:
                                self.definitions.add('message', flowmodel)
                            # add dielement
                            self.diplane.add('dielement', flow.dielement)
                            # hide help panel
                            self.hide_help_panel()
                        else:
                            # name getter
                            getname = lambda guielement: guielement.element.__class__.__name__
                            # retrieve names
                            e1name, e2name = getname(self.SELECTED_ELEMENT), getname(previous_selected)
                            # show message error
                            self.show_help_panel(f'Sorry, a connection cannot be made between <{e1name}> and <{e2name}>', danger)
                        # finish linking
                        self.set_mode(self.DRAG_MODE)

        # single right click
        def action_mouse_rclick(e):
            # select element
            self.SELECTED_ELEMENT = self.find_element(self.select_element(e.x, e.y))
            # prepare menu command
            def showmenu():  
                # adjust menu coords
                menu_coords = self.to_window_coords(e.x_root, e.y_root)
                # prepare options
                opts = [
                    {
                        'text': 'Delete',
                        'icon': 'delete.png',
                        'fg': danger,
                        'cmnd': lambda e: self.remove_element(self.SELECTED_ELEMENT)
                    },
                    {
                        'text': 'Change Name',
                        'icon': 'text.png',
                        'cmnd': lambda e: self.show_input(e.x_root, e.y_root, self.SELECTED_ELEMENT.set_text)
                    },
                    {
                        'text': 'Associate',
                        'icon': 'associate.png',
                        'cmnd': self.close_menu_after(lambda e: self.set_mode(self.LINK_MODE))
                    },
                    {
                        'text': 'Dissociate',
                        'icon': 'cut.png',
                        'cmnd': self.close_menu_after(lambda e: self.unlink_element(self.SELECTED_ELEMENT))
                    }
                ]
                # if it's a process
                if isinstance(self.SELECTED_ELEMENT, GUIProcess):
                    if len (self.definitions.elements['process']) == 1:
                        opts.pop(0)
                # adjust options, if this is a lane, remove 'associate' options
                if isinstance(self.SELECTED_ELEMENT, GUILane):
                    opts.pop(2)
                # if the element has no flows, remove 'dissociate'
                if len (self.SELECTED_ELEMENT.flows) == 0:
                    opts.pop()
                # if the element is a container
                if isinstance(self.SELECTED_ELEMENT, GUIContainer) == True:
                    if not isinstance(self.SELECTED_ELEMENT, GUILane):
                        opts.append({
                            'text': 'Resize',
                            'icon': 'resize.png',
                            'cmnd': self.close_menu_after(lambda e: self.set_mode(self.RESIZE_MODE))
                        })
                # if the element has options
                if self.SELECTED_ELEMENT.get_options() != None:
                    # retrieve element options
                    for e_opt in self.SELECTED_ELEMENT.get_options():
                        # save before
                        def save_before(command):
                            # save undo checkpoint
                            self.save_checkpoint(EditorWindow.ACTION_HIST['undo'])
                            # reassign canvas
                            self.assign_canvas_all()
                            # call command
                            command(None)
                        # adjust
                        def adjust_option_command(option):
                            # retrieve command of option
                            command = option['cmnd']
                            option['cmnd'] = lambda e: save_before(command)
                        # fix option command
                        adjust_option_command(e_opt)
                        # append
                        opts.append(e_opt)
                # show menu
                self.show_menu(x=menu_coords[0], y=menu_coords[1], options=opts)
            # starting a thread
            if self.SELECTED_ELEMENT != None:
                Thread(target=showmenu).start()

        # mouse moving
        def action_mouse_move(e):
            if self.SELECTED_MODE in [self.DRAG_MODE, self.CREATE_MODE]:
                if self.DRAG_ELEMENT != None:
                    # if the mode is specifically drag mode
                    if self.SELECTED_MODE == self.DRAG_MODE:
                        if not self.IS_DRAGGING:
                            self.IS_DRAGGING = True
                            # save check point
                            self.save_checkpoint(EditorWindow.ACTION_HIST['undo'])
                            # re assign canvas
                            self.assign_canvas_all()
                    # if the drag element is a lane, switch to its process instead
                    if isinstance(self.DRAG_ELEMENT, GUILane) == True:
                        self.DRAG_ELEMENT = self.DRAG_ELEMENT.guiprocess
                    # hide menu
                    self.hide_component('frm_menu')
                    # drag element
                    self.DRAG_ELEMENT.bring_front()
                    self.DRAG_ELEMENT.move(e.x, e.y)
                    # change cursor
                    self.cnv_canvas.config(cursor='hand2')
            if self.SELECTED_MODE == self.RESIZE_MODE:
                # calculate width & height
                w, h = abs(e.x - self.SELECTED_ELEMENT.x), abs(e.y - self.SELECTED_ELEMENT.y)
                # update element's size
                self.SELECTED_ELEMENT.resize(w, h)

        # mouse release
        def action_mouse_release(e):
            # check if there's a container behind
            container: GUIContainer = None
            # find container in canvas
            checkList = list(self.cnv_canvas.find_overlapping(e.x - 2, e.y - 2, e.x + 2, e.y + 2))
            checkList.reverse()
            for i in checkList:
                # find the whole element
                element = self.find_element(i)
                if isinstance(element, GUIContainer) == True and element != self.DRAG_ELEMENT:
                    container = element
                    break
            # if a container is found, append the element to that container
            if self.DRAG_ELEMENT != None:
                # if this container is not the parent, then erase all flows
                if self.DRAG_ELEMENT.parent != container:
                    # before disposing of flows, make sure that message flows get erased
                    self.unlink_element(self.DRAG_ELEMENT)
                # if the element already had a parent, 
                if self.DRAG_ELEMENT.parent != None:
                    self.DRAG_ELEMENT.parent.remove_child(self.DRAG_ELEMENT)
                # append the element to the new container
                if container != None:
                    container.append_child(self.DRAG_ELEMENT)
            # reset
            if self.SELECTED_MODE != self.CREATE_MODE:
                self.DRAG_ELEMENT = None
                self.IS_DRAGGING = False
            # reset mode if the selected mode is not a long term mode
            if self.SELECTED_MODE not in [self.SELECT_MODE, self.MOVE_MODE]:
                self.set_mode(self.DRAG_MODE)

        # key press 
        def action_key_press(e):
            # passing condition
            if self.SELECTED_MODE == self.MOVE_MODE:
                f = 0.0175
                if e.keysym == 'Right':
                    if self.MOVE_SCALE[0] + f <= 1:
                        self.MOVE_SCALE[0] += f
                elif e.keysym == 'Left':
                    if self.MOVE_SCALE[0] - f >= 0:
                        self.MOVE_SCALE[0] -= f
                elif e.keysym == 'Up':
                    if self.MOVE_SCALE[1] - f >= 0:
                        self.MOVE_SCALE[1] -= f
                elif e.keysym == 'Down':
                    if self.MOVE_SCALE[1] + f <= 1:
                        self.MOVE_SCALE[1] += f
                # update view
                self.update_view()
            # escape key
            if e.keysym == 'Escape':
                if self.SELECTED_MODE == self.CREATE_MODE:
                    # cancel creation
                    self.remove_element(self.DRAG_ELEMENT)
                    self.DRAG_ELEMENT = None
                # reset mode
                self.set_mode(self.DRAG_MODE)

        # if the user has no right to edit
        if self.get_privilege() != 'edit':
            self.hide_tools()
            self.show_help_panel('You don\'t have the right to edit this diagram!', danger)
            return

        # bind events
        self.cnv_canvas.bind('<Button-1>', action_mouse_click)
        self.cnv_canvas.bind('<Button-3>', action_mouse_rclick)
        self.cnv_canvas.bind('<Motion>', action_mouse_move)
        self.cnv_canvas.bind('<B1-Motion>', action_mouse_move)
        self.cnv_canvas.bind('<ButtonRelease-1>', action_mouse_release)
        self.cnv_canvas.bind_all('<Key>', action_key_press)
        self.cnv_canvas.bind_all('<Control-z>', lambda e: self.undo())
        self.cnv_canvas.bind_all('<Control-y>', lambda e: self.redo())
        self.cnv_canvas.bind_all('<Control-0>', lambda e: self.reset_zoom())
        self.cnv_canvas.bind_all('<Control-v>', lambda e: self.reset_view())
        self.cnv_canvas.bind_all('<Control-s>', lambda e: self.save_work())

    # a searching method to find the corresponding gui element from the given id
    def find_element(self, id):
        for guie in self.guielements:
            if guie.match(id) != None:
                return guie.match(id)
        return None
    
    # a searching method; it uses the model element as criteria
    def find_guielement_by_element(self, element):
        for guie in self.guielements:
            if guie.element.id == element.id:
                return guie
        return None

    # unlink an element
    def unlink_element(self, element):
        # save undo checkpoint
        self.save_checkpoint(EditorWindow.ACTION_HIST['undo'])
        # re assign canvas
        self.assign_canvas_all()
        # remove from parent and di container
        for flow in element.flows:
            # remove from di plane
            self.diplane.nokey_remove(flow.dielement)
            # remove from container
            if element.parent != None:
                # if this is a message flow then remove it from collaboration
                if flow.element.get_tag() == 'messageflow':
                    self.definitions.remove('message', flow.element)
                elif flow.element.get_tag() == 'sequenceflow':
                    element.parent.element.remove('flow', flow.element)
        # unlink target
        element.unlink()

    # delete an element
    def remove_element(self, element):
        # save undo checkpoint
        self.save_checkpoint(EditorWindow.ACTION_HIST['undo'])
        # emphasize that this element has a canvas
        self.assign_canvas_all()
        # if this is a lane
        guiprocess = None
        if isinstance (element, GUILane):
            guiprocess = element.guiprocess
            for child in element.children:
                self.remove_element(child)
        # remove flow links
        self.unlink_element(element)
        # remove the drawn element
        element.destroy()
        # remove from list
        if element in self.guielements:
            self.guielements.remove(element)
        # remove from plane
        self.diplane.nokey_remove(element.dielement)
        # if it's a process
        if isinstance (element, GUIProcess) == True:
            self.definitions.remove('process', element.element)
        # if this element is inside a container
        if element.parent != None:
            element.parent.remove_child(element)
        # if this was a lane, then guiprocess shouldn't be None
        if guiprocess != None:
            if len(guiprocess.lanes) == 1:
                self.remove_element(guiprocess.lanes[0])
        # hide menu
        self.hide_component('frm_menu')
    
    # delete selected elements button
    def btn_delete_selected_click(self):
        # save undo checkpoint
        self.save_checkpoint(EditorWindow.ACTION_HIST['undo'])
        # delete each selected element
        for element in self.SELECTED_ELEMENTS:
            self.remove_element(element)
            # delete unintentional checkpoint
            EditorWindow.ACTION_HIST['undo'].pop()

    # auto close menu
    def close_menu_after(self, callable):
        def cmnd(e):
            callable(e)
            self.hide_component('frm_menu')
        return cmnd 

    # show entry 
    def show_input(self, x, y, onReturn=None):
        # change mode
        self.set_mode(self.DRAG_MODE)
        # hide menu component
        self.hide_component('frm_menu')
        # create an input if there's none
        if hasattr(self, 'txt_input') == False:
            self.txt_input = TextBox(self, 'resources/icons/ui/text.png')
        # clean entry
        self.txt_input.clear()
        # set foucs
        self.txt_input.entry.focus()
        # prepare a command
        def inputReturn(e):
            # save undo checkpoint
            self.save_checkpoint(EditorWindow.ACTION_HIST['undo'])
            # re assign canvas
            self.assign_canvas_all()
            # change gui element's text
            onReturn(self.txt_input.get_text())
            # hide input
            self.hide_component('txt_input')
        # bind 
        self.txt_input.entry.unbind('<Return>')
        if onReturn != None:
            self.txt_input.entry.bind('<Return>', inputReturn)
        # convert the relative position to world position
        worldPos = self.to_window_coords(x, y)
        self.txt_input.place(x=worldPos[0], y=worldPos[1])

    # zooming functionalities
    def zoom_in(self):
        self.ZOOM_SCALE = abs (self.ZOOM_SCALE)
        self.zoom()

    def zoom_out(self):
        self.ZOOM_SCALE = -1 * abs (self.ZOOM_SCALE)
        self.zoom()

    def zoom(self):
        for guie in self.guielements:
            guie.scale(self.ZOOM_SCALE)

    def reset_zoom(self):
        self.ZOOM_SCALE = 6
        self.zoom()

    # BOOKMARK for kalai: saving functionality
    def save_work(self):

        # plane adjustment
        self.diplane.element = self.definitions.collaboration

        # logging save changes
        from pprint import pprint
        savefile = open('resources/temp/savelog.xml', 'w')
        # print the content of the new file  
        Thread(target=lambda: savefile.write(to_pretty_xml(self.definitions.serialize()))).start()

        # BOOKMARK_TOCHANGE: uncomment those
        if self.get_privilege() == 'read':
            MessageModal(self, 'Can\'t save changes', message='you don\'t have the right to edit this project!', messageType='error')
        else:
            date = datetime.now()
            # get project of subject
            project = self.subject if self.subject.__class__ == Project else self.subject.project
            # update project
            project.file = elementtobytes(self.definitions.serialize())
            project.lastEdited = date
            history = History(editDate=date, file=project.file, editor=EditorWindow.ACTIVE_USER, project=project)
            # get image and affect it
            self.take_screenshot(project, history)
            # save entity
            Container.save(project, history)

    def back_to_subject(self):
        def back(msg):
            msg.destroy()
            if self.subject.__class__ == Session: 
                self.windowManager.run_tag('collaboration', session=self.subject)
            else: 
                self.windowManager.run_tag('project', project=self.subject) if self.subject.owner == EditorWindow.ACTIVE_USER else self.windowManager.run_tag('home')

        self.show_prompt('Are you sure you want to leave this window?', lambda e: back(msg), 'Quit Prompt')

    # linking funcs
    def can_link(self, source, target):
        # lanes can't be linked
        if isinstance(source, GUILane) == True or isinstance(target, GUILane) == True:
            return False
        # you can't link a process with its child
        if isinstance(source, GUIProcess) == True or isinstance(target, GUIProcess) == True:
            # retrieve processes
            process = source if isinstance(source, GUIProcess) == True else target
            other = source.get_process() if isinstance(target, GUIProcess) == True else target.get_process()
            # compare processes
            if process == other:
                return False

        return True

    # responsible for figuring out which data model to use
    def get_link_model(self, source, target):
        """
        Figure out which model to use in this case
        """
        # preparations
        artifacts = [GUIDataObject, GUIDataStore]
        # data association case
        if type(source) in artifacts or type(target) in artifacts:
            # figure out sides
            linkable, artifact = source, target
            if type(target) in artifacts:
                linkable, artifact = source, target
            else:
                linkable, artifact = target, source
            # return 
            return linkable.element.link_data(artifact.element, (DataAssocDirection.IN if type(source) in artifacts else DataAssocDirection.OUT))
        # message flow case
        c1 = source.get_process() != target.get_process()
        c2 = len (self.definitions.elements['process']) > 0
        c3 = isinstance(source, GUIProcess) and isinstance(target, GUIProcess)
        if (c1 == True and c2 == True) or c3:
            return MessageFlow(source=source.element, target=target.element)
        # sequence flow case
        return source.element.add_link(target.element)

    # REDO/UNDO Actions
    def get_memento(self):
        return Memento(
            guielements=self.guielements,
            definitions=self.definitions,
            didiagram=self.didiagram,
            diplane=self.diplane
        )

    def save_checkpoint(self, collection: list):
        # revoke canvas from all elements
        self.revoke_canvas()
        # serializing the whole editor object
        serialized_data = pk.dumps(self.get_memento())
        # append
        collection.append(serialized_data)

    def load_checkpoint(self, memento):
        # update properties
        self.guielements = memento.guielements
        self.definitions = memento.definitions
        self.didiagram = memento.didiagram
        self.diplane = memento.diplane
        # reset editor settings
        self.set_mode(self.DRAG_MODE)
        self.reset_view()
        self.ZOOM_SCALE = 6
        # reset
        self.reset()

    def do(self, _from: list, _to: list):
        # skip if there's no checkpoint to retrieve
        if len(_from) == 0: return
        # save this current checkpoint
        self.save_checkpoint(_to)
        # deserialize checkpoint & load retrieved checkpoint
        self.load_checkpoint(pk.loads(_from.pop()))
        
    def undo(self):
        self.do(EditorWindow.ACTION_HIST['undo'], EditorWindow.ACTION_HIST['redo'])
    
    def redo(self):
        self.do(EditorWindow.ACTION_HIST['redo'], EditorWindow.ACTION_HIST['undo'])

    def assign_canvas(self, element):
        # emphasize that all elements have canvas
        element.canvas = self.cnv_canvas
        # their flows too
        for f in element.flows:
            f.canvas = self.cnv_canvas
        # if this e is a process
        if isinstance(element, GUIProcess):
            for lane in element.lanes:
                lane.canvas = self.cnv_canvas
                for child in lane.children:
                    self.assign_canvas(child)
    
    def assign_canvas_all(self):
        for e in self.guielements:
            self.assign_canvas(e)

    def revoke_canvas(self):
        # cannot let the canvas ruin the serialization process
        for g in self.guielements:
            # special memento setup 
            g.memento_setup()

    # Help Panel actions
    def show_help_panel(self, text, fgColor=black):
        # show help panel
        self.frm_help.pack_configure(side=TOP, padx=20, pady=20)
        # change label settings
        self.lbl_help.config(text=text, fg=fgColor)

    def hide_help_panel(self):
        self.frm_help.pack_forget()

    # draw from deserialization
    def get_gui_prefab(self, element):
        # retrieve tag
        tag = element.get_tag ()
        # switch
        if tag == 'task':
            return GUITask
        elif tag == 'event':
            return GUIEvent
        elif tag == 'gateway':
            return GUIGateway
        elif tag == 'process':
            return GUIProcess
        elif tag == 'subprocess':
            return GUISubProcess
        elif tag == 'lane':
            return GUILane
        elif tag == 'datastore':
            return GUIDataStore
        elif tag == 'dataobject':
            return GUIDataObject
        elif tag in ['sequenceflow', 'messageflow', 'dataassociation', 'association']:
            return GUIFlow
        return None

    # drawing diagram based on xml file
    def draw_diagram(self, byte_data):
        root_element = bytestoelement(byte_data)
        # instantiate a deserializer
        deserializer = Deserializer(root_element)
        # retrieve a definitions instance
        self.definitions = deserializer.definitions
        self.didiagram = deserializer.didiagram
        self.diplane = deserializer.diplane
        # show the content
        # print ('----- After Deserializing:')
        loadfile = open('resources/temp/loadlog.xml', 'w')
        loadfile.write (to_pretty_xml(self.definitions.serialize()))
        # draw all elements
        for e in deserializer.all_elements:
            # retrieve gui prefab class
            _class = self.get_gui_prefab(e)
            # skip flows
            if _class in [None, GUIFlow]:
                continue
            # get di element
            de = deserializer.delements.get(e.id if _class != GUIProcess else e.participant, None)
            xPos, yPos = 0, 0
            # check before proceeding
            if de == None:
                print ('Display Error: Failed to retrieve di element for', e.id)
                continue
            # prepare position
            xPos, yPos = int(float(de.bounds.x)), int(float(de.bounds.y))
            # instantiate
            prefab = _class (canvas=self.cnv_canvas, element=e, dielement=de)
            # change the size in case of containers
            if _class in [GUIProcess, GUISubProcess]:
                if de != None:
                    prefab.WIDTH, prefab.HEIGHT = int(float(de.bounds.width)), int(float(de.bounds.height))
            prefab.draw_at (xPos, yPos)
            # save instance
            self.guielements.append(prefab)
        # draw their flows
        for f in deserializer.all_elements:
            # if this is a data association just skip
            if isinstance(f, DataAssociation):
                continue
            # retrieve gui prefab class
            _class = self.get_gui_prefab(f)
            # if it's not a flow, skip it
            if _class != GUIFlow:
                continue
            # retrieve di element
            de = deserializer.delements.get(f.id, None)
            # find gui source & target
            guisrc = self.find_guielement_by_element(f.source)
            guitrg = self.find_guielement_by_element(f.target)
            # instantiate prefab
            prefab = _class(guisource=guisrc, guitarget=guitrg, element=f, dielement=de, canvas=self.cnv_canvas)
            prefab.draw_at(0, 0)
        # draw data associations
        for e in deserializer.all_elements:
            if hasattr(e, 'elements'):
                # draw data associations if there are any
                if 'dataAssociation' in e.elements:
                    for da in e.elements['dataAssociation']:
                        # find gui ends
                        guisrc, guitrg = self.find_guielement_by_element(e), self.find_guielement_by_element(da.target)
                        # draw flow
                        daflow = GUIFlow(canvas=self.cnv_canvas, guisource=guisrc, guitarget=guitrg, element=da, dielement=deserializer.delements.get(da.id, None))
                        daflow.draw_at(0, 0)
        # set up processes & subprocesses
        for guicontainer in self.guielements:
            # skip other gui elements
            if isinstance(guicontainer, GUIContainer) == False:
                continue
            # elements to append
            children = []
            toClear = []
            # setting up lanes
            if isinstance(guicontainer, GUIProcess):
                if 'lane' in guicontainer.element.elements:
                    for lane in guicontainer.element.elements['lane']:
                        guicontainer.add_lane(lane, False)
            # loop through its element's children
            if isinstance(guicontainer, GUISubProcess) or (isinstance (guicontainer, GUIProcess) and len (guicontainer.lanes) == 0):
                for key in guicontainer.element.elements.keys():
                    # skip flows
                    if key in ['flow', 'lane']:
                        continue
                    # loop through this collection
                    for child_element in guicontainer.element.elements[key]:
                        # find gui element of this element
                        guie = self.find_guielement_by_element(child_element)
                        # add it to the container
                        if guie != None:
                            children.append(guie)
                        else:
                            print ('Display Error: Failed to find the GUI element for', child_element.id)
                            toClear.append([key, child_element])
            else:
                for guilane in guicontainer.lanes:
                    for key in guilane.element.elements:
                        for node in guilane.element.elements[key]:
                            # find the element 
                            guinode = self.find_guielement_by_element(node)
                            # establish child-parent relationship
                            guilane.children.append(guinode)
                            guinode.parent = guilane
            # to avoid some runtime errors concerning dictionary size change
            for child in children:
                guicontainer.append_child(child)
            # clear the elements that are just extra hindrances
            for pair in toClear:
                guicontainer.element.remove(pair[0], pair[1])
            # redraw
            guicontainer.erase()
            guicontainer.draw()
        # assign canvas
        self.assign_canvas_all()

    # saving a jpg/png image
    def take_screenshot(self, *subjects):
        # this activity should be ran in another thread
        def runnable():
            # reset canvas position
            self.reset_view()
            # hide help panel
            self.hide_help_panel()
            # hide tools
            self.hide_tools()
            # change canvas background color
            self.cnv_canvas.config(bg=white)
            # pause thread
            sleep(0.5)
            # take a screen shot
            x0, y0 = self.cnv_canvas.winfo_rootx(), self.cnv_canvas.winfo_rooty()
            x1, y1 = x0 + self.cnv_canvas.winfo_width(), y0 + self.cnv_canvas.winfo_height()
            # save it
            ImgGrb.grab().crop((x0, y0, x1, y1)).save('resources/temp/shot.png')
            # BOOKMARK  affect it to its corresponding db record
            for subject in subjects:
                if subject != None: subject.image = filetobytes('resources/temp/shot.png')
            # show tools again
            self.show_tools()
            # change back the canvas bg
            self.cnv_canvas.config(bg=background)
            # inform the user
            self.show_help_panel('A screenshot was taken before saving', teal)
        # start screenshot thread
        Thread(target=runnable).start()
    
    # get privilege
    def get_privilege(self):
        return 'edit' if self.subject.owner == EditorWindow.ACTIVE_USER else (Container.filter(ShareLink, ShareLink.projectId == self.subject.id).first() if self.subject.__class__ == Project else Container.filter(Collaboration, Collaboration.sessionId == self.subject.id, Collaboration.userId == EditorWindow.ACTIVE_USER.id).first()).privilege