from tkinter import *
from resources.colors import *
from views.windows.abstract.tabbedwindow import TabbedWindow
from views.components.listitem import ListItem
from views.components.icon import IconFrame
from views.components.iconbuttonfactory import *
from views.components.scrollable import Scrollable

class HomeWindow(TabbedWindow):

    PROJECT_LI = 0
    SESSION_LI = 1

    tabSettings = [
        {   
            'icon': 'folder.png',
            'text': 'My Projects',
            'tag': 'tb_projects'
        },
        {   
            'icon': 'session.png',
            'text': 'My Sessions',
            'tag': 'tb_sessions'
        }
    ]

    def __init__(self, root, **args):
        TabbedWindow.__init__(self, root, HomeWindow.tabSettings, 'Welcome', **args)

        # Design elements
        self.design()

    def design(self):
        # lay out the components to project tab
        self.btn_container1 = Frame(self.tb_projects, bg=background, pady=10)
        self.btn_container1.pack (side=TOP, fill=X)

        self.btn_create_project = MainButton(self.btn_container1, 'Create New Project', 'new_project.png')
        self.btn_create_project.pack(side=LEFT, padx=(0, 10))
        
        self.btn_open = SecondaryButton(self.btn_container1, 'Open XML-BPMN File From Device', 'upload.png')
        self.btn_open.pack(side=LEFT)

        self.scr_list_view1 = Scrollable(self.tb_projects, bg=background, pady=15)
        self.scr_list_view1.set_gridcols(4)
        self.scr_list_view1.pack(fill=BOTH, expand=1)

        # BOOKMARK: fill project items
        for i in range(4):
            self.scr_list_view1.grid_item(None, {'username': 'Ibrahim'}, None, lambda item: HomeWindow.create_list_item(item), 15)

        # lay out the components to session tab
        self.btn_container2 = Frame(self.tb_sessions, bg=background, pady=10, padx=1)
        self.btn_container2.pack (side=TOP, fill=X)

        self.btn_create_session = MainButton(self.btn_container2, 'Create New Session', 'new_session.png')
        self.btn_create_session.pack(side=LEFT, padx=(0, 10))

        self.scr_list_view2 = Scrollable(self.tb_sessions, bg=background, pady=15)
        self.scr_list_view2.set_gridcols(4)
        self.scr_list_view2.pack(fill=BOTH, expand=1)

        # BOOKMARK: fill session items
        for i in range(4):
            self.scr_list_view2.grid_item(None, {'username': 'Ibrahim'}, None, lambda item: HomeWindow.create_list_item(item, HomeWindow.SESSION_LI), 15)

    def create_list_item(item: ListItem, liType: int = PROJECT_LI):
        item.configure (highlightthickness=1, highlightbackground=border, bg=white)

        img_size = 205
        img_thumb = Frame(item, height=img_size, bg=white)
        img_thumb.pack_propagate(0)

        border_bottom = Frame(item, bg=border)
        frm_info = Frame(item, bg=silver, padx=10, pady=10)
        frm_details = Frame(frm_info, bg=silver)
        
        Label(frm_info, text='Title', bg=silver, fg=black, font='-size 18').pack(side=TOP, fill=X, pady=(0, 10))

        panel_settings = [
            {
                'label': 'Created In:',
                'text': '2020-5-27'
            },
            {
                'label': 'Edited In:',
                'text': 'Yesterday'
            }
        ]

        if liType == HomeWindow.SESSION_LI:
            panel_settings.append({
                'label': 'Members:',
                'text': 'XX'
            })

        for i in panel_settings:
            frm = Frame(frm_details, bg=silver)
            frm.pack(side=LEFT, fill=X, expand=1)
            Label(frm, text=i.get('label'), fg=teal, bg=silver, font='-size 8').pack(fill=X)
            Label(frm, text=i.get('text'), fg=gray, bg=silver, font='-size 9').pack(fill=X)
        
        img_thumb.pack(fill=X, side=TOP)
        border_bottom.pack(fill=X, side=TOP)
        frm_info.pack(fill=X, side=TOP)
        frm_details.pack(fill=X, side=TOP)

        IconFrame(item, 'resources/icons/ui/menu.png', 8, teal, 32, bg=white).place(relx=1-0.03, rely=0.02, anchor=N+E)

