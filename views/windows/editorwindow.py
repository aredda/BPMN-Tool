from tkinter import *
from resources.colors import *
from views.windows.abstract.sessionwindow import SessionWindow
from views.components.scrollable import Scrollable
from views.components.listitem import ListItem
from views.components.icon import IconFrame
from views.components.textbox import TextBox
from views.factories.iconbuttonfactory import *
from views.prefabs.abstract.guicontainer import GUIContainer
from views.prefabs.guievent import GUIEvent
from views.prefabs.guigateway import GUIGateway
from views.prefabs.guisubprocess import GUISubProcess
from views.prefabs.guitask import GUITask
from views.prefabs.guiprocess import GUIProcess
from views.prefabs.guidatastore import GUIDataStore
from views.prefabs.guidataobject import GUIDataObject
from views.prefabs.guiflow import GUIFlow
from threading import Thread

class EditorWindow(SessionWindow):
    
    toolSettings = {
        LEFT: {
            'size': 35,
            'path': 'resources/icons/ui/',
            'tools': [
                { 'icon': 'save.png' },
                { 'icon': 'open.png', 'bg': danger }
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
                { 'icon': 'redo.png' },
                { 'icon': 'undo.png' },
                { 'icon': 'move.png' },
                { 'icon': 'select.png' },
                { 'icon': 'zoom_in.png' },
                { 'icon': 'zoom_out.png' }
            ]
        }
    }

    # EDITOR Modes
    DRAG_MODE = 0
    SELECT_MODE = 1
    MOVE_MODE = 2
    CREATE_MODE = 3
    LINK_MODE = 4
    RESIZE_MODE = 5

    def __init__(self, root, subject=None, **args):
        SessionWindow.__init__(self, root, **args)

        self.subject = subject
        self.guielements = []

        self.SELECTED_MODE = self.DRAG_MODE
        self.SELECTED_ELEMENT = None
        
        self.DRAG_ELEMENT = None

        self.design()
        self.setup_actions()

    def setup_tools(self):
        # Lay out tool panels
        for i in EditorWindow.toolSettings.keys():

            settings = EditorWindow.toolSettings[i]

            frm_container = Frame(self.cnv_canvas, bg=white, highlightthickness=1, highlightbackground=border, padx=10, pady=10)
            frm_container.pack(side=i, padx=20, pady=20)

            for j in settings['tools']:

                align = settings.get('align', TOP)
                spacing = { 'padx': 0 if align == TOP else (0, 5), 'pady': 0 if align != TOP else (0, 5) }

                # process command
                cmnd = None
                for t in ['create', 'do']:
                    if t in j: 
                        cmnd = self.select_event(t, j.get(t))

                ic_tool = IconFrame(frm_container, settings['path'] + j.get('icon'), 15, j.get('bg', settings.get('bg', black)), settings['size'], cmnd, settings.get('hoverBg', None), bg=white)
                ic_tool.pack(side=align) 

                if settings['tools'].index(j) != len(settings['tools']) - 1:
                    ic_tool.pack(side=align, **spacing)
    
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

    def setup_actions(self):
        
        # single click
        def action_mouse_click(e):
            justCreated = False
            # finish creation
            if self.SELECTED_MODE == self.CREATE_MODE:
                # reset mode
                self.set_mode(self.DRAG_MODE)
                # mark as 'just created'
                justCreated = True
                
            # finish resizing
            if self.SELECTED_MODE == self.RESIZE_MODE:
                self.set_mode(self.DRAG_MODE)
            # hide components
            self.hide_component('frm_menu')
            self.hide_component('txt_input')
            # save the previous selected element
            previous_selected = self.SELECTED_ELEMENT
            # find gui element that has this element id
            self.SELECTED_ELEMENT = self.DRAG_ELEMENT = self.find_element(self.select_element(e.x, e.y))
            # linking elements
            if self.SELECTED_ELEMENT != None and justCreated == False:
                # if an element is selected
                if self.SELECTED_MODE == self.LINK_MODE:
                    if self.SELECTED_ELEMENT != previous_selected:
                        # creating a flow
                        flow = GUIFlow(canvas=self.cnv_canvas, guisource=previous_selected, guitarget=self.SELECTED_ELEMENT)
                        flow.draw_at(0, 0)
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
                    # hide menu
                    self.hide_component('frm_menu')
                    # drag element
                    self.DRAG_ELEMENT.bring_front()
                    self.DRAG_ELEMENT.move(e.x, e.y)
            if self.SELECTED_MODE == self.RESIZE_MODE:
                # calculate width & height
                w, h = abs(e.x - self.SELECTED_ELEMENT.x), abs(e.y - self.SELECTED_ELEMENT.y)
                # update element's size
                self.SELECTED_ELEMENT.resize(w, h)

        # mouse release
        def action_mouse_release(e):
            # check if there's a container behind
            container: GUIContainer = None
            checked = self.cnv_canvas.find_overlapping(e.x - 2, e.y - 2, e.x + 2, e.y + 2)
            for item in checked:
                element = self.find_element(item)
                if isinstance(element, GUIContainer) == True and element != self.DRAG_ELEMENT:
                    container = element
                    break
            if container != None:
                container.append_child(self.DRAG_ELEMENT)
            # reset
            if self.SELECTED_MODE != self.CREATE_MODE:
                self.DRAG_ELEMENT = None

        self.cnv_canvas.bind('<Button-1>', action_mouse_click)
        self.cnv_canvas.bind('<Button-3>', action_mouse_rclick)
        self.cnv_canvas.bind('<Motion>', action_mouse_move)
        self.cnv_canvas.bind('<B1-Motion>', action_mouse_move)
        self.cnv_canvas.bind('<ButtonRelease-1>', action_mouse_release)
        
    def select_event(self, tag, value):
        # create event
        if tag == 'create':
            # prepare create command
            def cmnd_create(e):
                # instantiate
                guie = value(canvas=self.cnv_canvas)
                # draw
                guie.draw_at(0, 0)
                # change mode
                self.SELECTED_MODE = self.CREATE_MODE
                # set as the drag element
                self.DRAG_ELEMENT = guie
                # appen
                self.guielements.append(guie)
            # return it
            return cmnd_create

    # a searching method to find the corresponding gui element from the given id
    def find_element(self, id):
        for guie in self.guielements:
            if id in guie.id:
                return guie
        return None

    # delete an element
    def remove_element(self, element):
        # remove the drawn element
        element.destroy()
        # remove from list
        self.guielements.remove(element)
        # hide menu
        self.hide_component('frm_menu')

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