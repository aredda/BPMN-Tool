from tkinter import *
from resources.colors import *
from views.windows.abstract.sessionwindow import SessionWindow
from views.components.scrollable import Scrollable
from views.components.listitem import ListItem
from views.components.icon import IconFrame
from views.factories.iconbuttonfactory import *
from views.prefabs.guievent import GUIEvent
from views.prefabs.guigateway import GUIGateway
from views.prefabs.guisubprocess import GUISubProcess
from views.prefabs.guitask import GUITask
from views.prefabs.guiprocess import GUIProcess

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
            'hoverBg': silver,
            'tools': [
                { 'icon': 'start-event.png', 'create': GUIEvent },
                { 'icon': 'gateway.png', 'create': GUIGateway },
                { 'icon': 'task.png', 'create': GUITask },
                { 'icon': 'subprocess-expanded.png', 'create': GUISubProcess },
                { 'icon': 'participant.png', 'create': GUIProcess },
                { 'icon': 'connection-multi.png' },
                { 'icon': 'data-object.png' },
                { 'icon': 'data-store.png' },
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
    MOVE_MODE = 0
    SELECT_MODE = 1

    def __init__(self, root, subject=None, **args):
        SessionWindow.__init__(self, root, **args)

        self.subject = subject
        self.guielements = []

        self.SELECTED_MODE = self.MOVE_MODE
        self.SELECTED_ELEMENT = None

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

    def setup_actions(self):
        
        # single click
        def action_mouse_click(e):
            # retrieve the last element (top element) to be found in the canvas
            last_element = self.cnv_canvas.find_overlapping(e.x - 2, e.y - 2, e.x + 2, e.y + 2)
            if len (last_element) > 0: last_element = last_element[-1]
            # find gui element that has this element id
            self.SELECTED_ELEMENT = self.find_element(last_element)

        # mouse moving
        def action_mouse_move(e):
            if self.SELECTED_MODE == self.MOVE_MODE:
                if self.SELECTED_ELEMENT != None:
                    self.SELECTED_ELEMENT.move(e.x, e.y)
                    self.SELECTED_ELEMENT.bring_front()

        # mouse release
        def action_mouse_release(e):
            self.SELECTED_ELEMENT = None

        self.cnv_canvas.bind('<Button-1>', action_mouse_click)
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
                guie.draw_at(256, 128)
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