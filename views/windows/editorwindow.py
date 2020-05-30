from tkinter import *
from resources.colors import *
from views.windows.abstract.sessionwindow import SessionWindow
from views.components.scrollable import Scrollable
from views.components.listitem import ListItem
from views.components.icon import IconFrame
from views.components.iconbuttonfactory import *

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
                { 'icon': 'start-event.png' },
                { 'icon': 'gateway.png' },
                { 'icon': 'task.png' },
                { 'icon': 'subprocess-expanded.png' },
                { 'icon': 'participant.png' },
                { 'icon': 'connection-multi.png' },
                { 'icon': 'data-object.png' },
                { 'icon': 'data-store.png' },
                { 'icon': 'group.png' },
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

    def __init__(self, root, subject=None, **args):
        SessionWindow.__init__(self, root, **args)

        self.subject = None

        self.setup_tools()

    def setup_tools(self):
        # Lay out tool panels
        for i in EditorWindow.toolSettings.keys():

            settings = EditorWindow.toolSettings[i]

            frm_container = Frame(self.frm_body, bg=white, highlightthickness=1, highlightbackground=border, padx=10, pady=10)
            frm_container.pack(side=i)

            for j in settings['tools']:

                align = settings.get('align', TOP)
                spacing = { 'padx': 0 if align == TOP else (0, 5), 'pady': 0 if align != TOP else (0, 5) }

                ic_tool = IconFrame(frm_container, settings['path'] + j.get('icon'), 15, j.get('bg', settings.get('bg', black)), settings['size'], j.get('cmnd', None), settings.get('hoverBg', None), bg=white)
                ic_tool.pack(side=align) 

                if settings['tools'].index(j) != len(settings['tools']) - 1:
                    ic_tool.pack(side=align, **spacing)
    
