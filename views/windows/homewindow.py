from tkinter import *
from resources.colors import *
from views.windows.abstract.tabbedwindow import TabbedWindow
from views.components.listitem import ListItem
from views.components.icon import IconFrame
from views.factories.iconbuttonfactory import *
from views.components.scrollable import Scrollable
from models.entities.Entities import *
from datetime import datetime

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
        # Load hardcoded data
        self.dummies()
        # Fill methods
        self.fill_projects(self.dataContainer['project'])

    def dummies(self):
        self.dataContainer = {
            'project': [
                Project(title='Situation 1', creationDate=datetime.now()),
                Project(title='BMPN Dgm', creationDate=datetime.now()),
                Project(title='Whatever', creationDate=datetime.now()),
                Project(title='Situation 2', creationDate=datetime.now()),
                Project(title='Another project', creationDate=datetime.now()),
                Project(title='Purchase Process', creationDate=datetime.now())
            ]
        }

    def design(self):
        # lay out the components to project tab
        self.btn_container1 = Frame(self.tb_projects, bg=background, pady=10)
        self.btn_container1.pack (side=TOP, fill=X)

        # BOOKMARK: modal redirections
        # configure redirections to form modals
        createProjectModalCmnd = lambda e: (self.windowManager.get_module('CreateProjectModal'))(
            self,
            # BOOKMARK: create project button command
            lambda formModal: print(formModal.get_form_data())
        )
        loadProjectModalCmnd = lambda e: (self.windowManager.get_module('LoadProjectModal'))(
            self,
            # BOOKMARK: create loaded project button command
            lambda formModal: print(formModal.get_form_data())
        )
        createSessionModalCmnd = lambda e: (self.windowManager.get_module('CreateSessionModal'))(
            self,
            # BOOKMARK: create project button command
            lambda formModal: print(formModal.get_form_data())
        )
        joinSessionModalCmnd = lambda e: (self.windowManager.get_module('JoinModal'))(
            self,
            # BOOKMARK: join session command
            lambda formModal: print(formModal.get_form_data())
        )
        joinProjectModalCmnd = lambda e: (self.windowManager.get_module('JoinModal'))(
            self,
            # BOOKMARK: join session command
            lambda formModal: print(formModal.get_form_data())
        )

        self.btn_create_project = MainButton(self.btn_container1, 'Create New Project', 'new_project.png', createProjectModalCmnd)
        self.btn_create_project.pack(side=LEFT, padx=(0, 10))
        
        self.btn_open = SecondaryButton(self.btn_container1, 'Load From Device', 'upload.png', loadProjectModalCmnd)
        self.btn_open.pack(side=LEFT, padx=(0, 10))
        
        self.btn_open = SecondaryButton(self.btn_container1, 'Access Project', 'login.png', joinProjectModalCmnd)
        self.btn_open.pack(side=RIGHT)

        self.lv_project = Scrollable(self.tb_projects, bg=background, pady=15)
        self.lv_project.set_gridcols(4)
        self.lv_project.pack(fill=BOTH, expand=1)

        # lay out the components to session tab
        self.btn_container2 = Frame(self.tb_sessions, bg=background, pady=10, padx=1)
        self.btn_container2.pack (side=TOP, fill=X)

        self.btn_create_session = MainButton(self.btn_container2, 'Create New Session', 'new_session.png', createSessionModalCmnd)
        self.btn_create_session.pack(side=LEFT, padx=(0, 10))
        
        self.btn_join_session = SecondaryButton(self.btn_container2, 'Join Session', 'login.png', joinSessionModalCmnd)
        self.btn_join_session.pack(side=RIGHT)

        self.lv_session = Scrollable(self.tb_sessions, bg=background, pady=15)
        self.lv_session.set_gridcols(4)
        self.lv_session.pack(fill=BOTH, expand=1)

    # BOOKMARK: fill project items
    def fill_projects(self, dataList: list):
        # cleaning up old items
        self.lv_project.empty()
        # refilling 
        for item in dataList:
            self.lv_project.grid_item(item, {'title': item.title, 'creationDate': item.creationDate}, None, lambda i: self.create_list_item(i), 15)

    # BOOKMARK: fill session items
    def fill_sessions(self, dataList: list):
        # cleaning up old items
        self.lv_project.empty()
        # refilling 
        for item in dataList:
            self.lv_session.grid_item(item, {'title': item.title, 'creationDate': item.creationDate}, None, lambda i: self.create_list_item(i, HomeWindow.SESSION_LI), 15)

    # BOOKMARK: Project List Item & Session List Item Creation Method
    def create_list_item(self, item: ListItem, liType: int = PROJECT_LI):
        item.configure (highlightthickness=1, highlightbackground=border, bg=white)

        img_size = 205
        img_thumb = Frame(item, height=img_size, bg=white)
        img_thumb.pack_propagate(0)

        border_bottom = Frame(item, bg=border)
        frm_info = Frame(item, bg=silver, padx=10, pady=10)
        frm_details = Frame(frm_info, bg=silver)
        
        Label(frm_info, text=item.bindings.get('title', '{title}'), bg=silver, fg=black, font='-size 18').pack(side=TOP, fill=X, pady=(0, 10))

        panel_settings = [
            {
                'label': 'Created In:',
                'text': item.bindings.get('creationDate').strftime('%a, %d %b') if 'creationDate' in item.bindings else '{creationDate}'
            },
            {
                'label': 'Edited In:',
                'text':  item.bindings.get('lastEdited').strftime('%a, %d %b') if 'lastEdited' in item.bindings else '{lastEdited}'
            }
        ]

        if liType == HomeWindow.SESSION_LI:
            panel_settings.append({
                'label': 'Members:',
                'text': item.bindings.get('memberCount', '{memberCount}')
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

        # BOOKMARK: project item's menu
        def options_menu(e):
            # convert screen mouse position
            win_coords = self.to_window_coords(e.x_root, e.y_root)
            # show menu
            self.show_menu(x=win_coords[0], y=win_coords[1], width=150, height=200, options=[
                {
                    'text': 'Open',
                    'icon': 'open.png',
                    'cmnd': lambda e: HomeWindow.li_command(item.dataObject)
                },
                {
                    'text': 'Share',
                    'icon': 'share.png'
                },
                {
                    'text': 'Delete',
                    'icon': 'delete.png'
                }
            ])
        # options icon
        IconFrame(item, 'resources/icons/ui/menu.png', 10, teal, 32, options_menu, bg=white).place(relx=1-0.03, rely=0.02, anchor=N+E)

    # BOOKMARK: this is how a COMMAND should be
    def li_command(dataObject):
        print ('You are operating in', dataObject.title)