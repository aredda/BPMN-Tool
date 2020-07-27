from tkinter import *
from resources.colors import *
from models.bpmn.definitions import Definitions
from models.bpmn.sequenceflow import SequenceFlow
from models.bpmn.messageflow import MessageFlow
from models.bpmn.dataassociation import DataAssociation, DataAssocDirection
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
from threading import Thread
from copy import copy, deepcopy

from helpers.xmlutility import elementtobytes, bytestoelement
from models.entities.Entities import Project, Session, Collaboration, ShareLink, History
from models.entities.Container import Container
from datetime import datetime
from views.windows.modals.messagemodal import MessageModal

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
                { 'icon': 'data-store.png', 'create': GUIDataStore },
                { 'icon': 'text-annotation.png' }
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
                { 'icon': 'move.png' },
                { 'name': 'btn_select_mode', 'icon': 'select.png', 'cmnd': 'enable_select_mode' },
                { 'icon': 'zoom_in.png', 'cmnd': 'zoom_in' },
                { 'icon': 'zoom_out.png', 'cmnd': 'zoom_out' }
            ]
        }
    }

    # command & event config method
    def select_event(self, tag, value):
        # create event
        if tag == 'create':
            # prepare create command
            def cmnd_create(e):
                # save checkpoint
                # self.save_checkpoint(self.undo_dict, self.guielements, self.definitions)
                # instantiate
                guie = value(canvas=self.cnv_canvas)
                # draw
                guie.draw_at(0, 0)
                # show help information
                self.show_help_panel('Hover over the position you want to instantiate on, then left-click to drop')
                # change mode
                self.set_mode(self.CREATE_MODE)
                # set as the drag element
                self.DRAG_ELEMENT = guie
                # append
                self.guielements.append(guie)
                if isinstance(guie, GUIProcess) == True:
                    self.definitions.add(guie.element.get_tag(), guie.element)
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

        # undo/redo actions
        self.undo_dict = { 'gui': [], 'def': [] }
        self.redo_dict = { 'gui': [], 'def': [] }

        # editor's gears
        self.SELECTED_MODE = self.DRAG_MODE
        self.SELECTED_ELEMENT = None
        self.SELECTED_ELEMENTS = []
        self.DRAG_ELEMENT = None
        self.ZOOM_SCALE = 6

        self.design()
        self.setup_actions()
        

    def setup_tools(self):
        # Lay out tool panels
        for i in EditorWindow.toolSettings.keys():
            # get the settings of this set of tools
            settings = EditorWindow.toolSettings[i]
            # prepare a container
            frm_container = Frame(self.cnv_canvas, bg=white, highlightthickness=1, highlightbackground=border, padx=10, pady=10)
            frm_container.pack(side=i, padx=20, pady=20)
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
        self.cnv_canvas = Canvas(self.frm_body, bg=background, highlightthickness=0)
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
        # change cursor
        if mode in [self.CREATE_MODE]:
            self.cnv_canvas.config(cursor='hand2')
        if mode in [self.RESIZE_MODE]:
            self.cnv_canvas.config(cursor='size_ne_sw')
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
            self.show_help_panel('Select an element in order to make a connection')            

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

    # responsible for refreshing all gui elements
    def reset(self):
        self.clear()
        for e in self.guielements:
            e.erase()
            e.draw()

    # takes care of clearing
    def clear(self):
        self.cnv_canvas.delete('all')    
        
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
                # if select mode is enabled
                if self.SELECTED_MODE == self.SELECT_MODE:
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
                            # save undo action
                            # self.save_checkpoint(self.undo_dict, self.guielements, self.definitions)
                            # generating a flow model
                            flowmodel = self.get_link_model(previous_selected, self.SELECTED_ELEMENT)
                            # creating a flow
                            flow = GUIFlow(canvas=self.cnv_canvas, guisource=previous_selected, guitarget=self.SELECTED_ELEMENT, element=flowmodel)
                            flow.draw_at(0, 0)
                            # if this model is a message flow
                            if isinstance(flowmodel, MessageFlow) == True:
                                self.definitions.add('message', flowmodel)
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
                    }
                ]
                # if the element is a container
                if isinstance(self.SELECTED_ELEMENT, GUIContainer) == True:
                    opts.append({
                        'text': 'Resize',
                        'icon': 'resize.png',
                        'cmnd': self.close_menu_after(lambda e: self.set_mode(self.RESIZE_MODE))
                    })
                # if the element has options
                if self.SELECTED_ELEMENT.get_options() != None:
                    opts += self.SELECTED_ELEMENT.get_options()
                # show menu
                self.show_menu(x=menu_coords[0], y=menu_coords[1], options=opts)
            # starting a thread
            if self.SELECTED_ELEMENT != None:
                Thread(target=showmenu).start()

        # mouse moving
        def action_mouse_move(e):
            if self.SELECTED_MODE in [self.DRAG_MODE, self.CREATE_MODE]:
                if self.DRAG_ELEMENT != None:
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
                # if the element already had a parent, 
                if self.DRAG_ELEMENT.parent != None:
                    self.DRAG_ELEMENT.parent.remove_child(self.DRAG_ELEMENT)
                self.DRAG_ELEMENT.parent = None
                # append the element to the new container
                if container != None:
                    self.DRAG_ELEMENT.parent = container
                    container.append_child(self.DRAG_ELEMENT)
            # reset
            if self.SELECTED_MODE != self.CREATE_MODE:
                self.DRAG_ELEMENT = None
            # reset mode if the selected mode is not a long term mode
            if self.SELECTED_MODE not in [self.SELECT_MODE]:
                self.set_mode(self.DRAG_MODE)

        # bind events
        self.cnv_canvas.bind('<Button-1>', action_mouse_click)
        self.cnv_canvas.bind('<Button-3>', action_mouse_rclick)
        self.cnv_canvas.bind('<Motion>', action_mouse_move)
        self.cnv_canvas.bind('<B1-Motion>', action_mouse_move)
        self.cnv_canvas.bind('<ButtonRelease-1>', action_mouse_release)

    # a searching method to find the corresponding gui element from the given id
    def find_element(self, id):
        for guie in self.guielements:
            if guie.match(id) != None:
                return guie.match(id)
        return None

    # delete an element
    def remove_element(self, element):
        # save undo checkpoint
        # self.save_checkpoint(self.undo_dict, self.guielements, self.definitions)
        # remove the drawn element
        element.destroy()
        # unlink all flows
        element.unlink()
        # remove from list
        if element in self.guielements:
            self.guielements.remove(element)
        # if it's a process
        if isinstance (element, GUIProcess) == True:
            self.definitions.remove('process', element.element)
        # hide menu
        self.hide_component('frm_menu')

    
    # delete selected elements button
    def btn_delete_selected_click(self):
        # delete each selected element
        for element in self.SELECTED_ELEMENTS:
            self.remove_element(element)

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
            onReturn(self.txt_input.get_text())
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

    # BOOKMARK for kalai: saving functionality
    def save_work(self):
        from helpers.stringhelper import to_pretty_xml
        from os import system

        clean = lambda e: system('cls')

        clean(None)
        print (to_pretty_xml(self.definitions.serialize()))
        
        # get privilege
        def get_privilege():
            if self.subject.owner == EditorWindow.ACTIVE_USER: return 'edit'
            else:
                obj = Container.filter(ShareLink, ShareLink.projectId == self.subject.id).first() if self.subject.__class__ == Project else Container.filter(Collaboration, Collaboration.sessionId == self.subject.id, Collaboration.userId == EditorWindow.ACTIVE_USER.id).first()
                return obj.privilege

        # BOOKMARK_TOCHANGE: uncomment those
        # if get_privilege() == 'read':
        #     MessageModal(self, 'can\'t save changes', message='you don\'t have the right to edit this project !', messageType='error')
        # else:
        #     newFile = elementtobytes(self.definitions.serialize())
        #     date = datetime.now()
        #     # get project of subject
        #     project = self.subject if self.subject.__class__ == Project else self.subject.project
        #     # update project
        #     project.file = newFile
        #     project.lastEdited = date
            
        #     Container.save(project, History(editDate=date, file=newFile, editor=EditorWindow.ACTIVE_USER, project=project))
        #     MessageModal(self, 'success', message='changes saved succesfully !', messageType='info')

        # # get etree from file  
        # print(to_pretty_xml(bytestoelement(project.file)))

    def back_to_subject(self):
        def back(msg):
            msg.destroy()
            if self.subject.__class__ == Session: self.windowManager.run_tag('collaboration', session=self.subject)
            else: self.windowManager.run_tag('project', project=self.subject) if self.subject.owner == EditorWindow.ACTIVE_USER else self.windowManager.run_tag('home')

        msg = MessageModal(self, title='confirmation', message='are you sure you want to leave this window ?', messageType='prompt', actions={'yes': lambda e: back(msg)})

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
        if (source.get_process() != target.get_process()) or (source.get_process() == None and target.get_process() == None):
            return MessageFlow(source=source.element, target=target.element)
        # sequence flow case
        return source.element.add_link(target.element)

    # REDO/UNDO Actions
    def save_checkpoint(self, trackdict, guicp, defcp):
        # clone elements
        clone = []
        for e in guicp:
            clone.append (copy(e))
        defclone = copy(defcp)
        # append
        trackdict['gui'].append (clone)
        trackdict['def'].append (defclone)

    def undo(self):
        action1 = self.undo_dict['gui'].pop()
        action2 = self.undo_dict['def'].pop()
        # save preferences in order to be able to redo them
        self.save_checkpoint(self.redo_dict, self.guielements, self.definitions)
        # undo
        self.guielements, self.definitions = action1, action2
        # reset canvas
        self.reset()
    
    def redo(self):
        action1 = self.redo_dict['gui'].pop()
        action2 = self.redo_dict['def'].pop()
        # save preferences in order to be able to undo them
        self.save_checkpoint(self.undo_dict, self.guielements, self.definitions)
        # undo
        self.guielements, self.definitions = action1, action2
        # reset canvas
        self.reset()

    # Help Panel actions
    def show_help_panel(self, text, fgColor=black):
        # show help panel
        self.frm_help.pack_configure(side=TOP, padx=20, pady=20)
        # change label settings
        self.lbl_help.config(text=text, fg=fgColor)

    def hide_help_panel(self):
        self.frm_help.pack_forget()