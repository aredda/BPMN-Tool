from tkinter import *
from resources.colors import *
from views.windows.abstract.tabbedwindow import TabbedWindow
from views.components.listitem import ListItem
from views.components.icon import IconFrame
from views.factories.iconbuttonfactory import *
from views.components.scrollable import Scrollable
from models.entities.Entities import *
from datetime import datetime, timedelta

from models.entities.Container import Container
from models.entities.Entities import Project, Session, User
from models.entities.enums.notificationtype import NotificationType
from models.entities.enums.notificationnature import NotificationNature
from views.windows.projectwindow import ProjectWindow
from views.windows.editorwindow import EditorWindow
from views.windows.collaborationwindow import CollaborationWindow
from views.windows.modals.messagemodal import MessageModal
import re
from helpers.filehelper import filetobytes
from helpers.imageutility import getdisplayableimage

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
        # Fill methods
        self.fill_projects()
        self.fill_sessions()


    def design(self):
        # lay out the components to project tab
        self.btn_container1 = Frame(self.tb_projects, bg=background, pady=10)
        self.btn_container1.pack (side=TOP, fill=X)

        # BOOKMARK: modal redirections
        # configure redirections to form modals
        createProjectModalCmnd = lambda e: (self.windowManager.get_module('CreateProjectModal'))(
            self,
            # BOOKMARK_DONE: create project button command
            lambda formModal: self.create(formModal)
        )
        loadProjectModalCmnd = lambda e: (self.windowManager.get_module('LoadProjectModal'))(
            self,
            # BOOKMARK_DONE: create load project button command
            lambda formModal: self.create(formModal, HomeWindow.PROJECT_LI, True)
        )
        createSessionModalCmnd = lambda e: (self.windowManager.get_module('CreateSessionModal'))(
            self,
            # BOOKMARK_DONE: create session button command
            lambda formModal: self.create(formModal, HomeWindow.SESSION_LI)
        )
        joinSessionModalCmnd = lambda e: (self.windowManager.get_module('JoinModal'))(
            self,
            # BOOKMARK_DONE: join session command
            lambda formModal: self.join_session(formModal)
        )
        joinProjectModalCmnd = lambda e: (self.windowManager.get_module('JoinModal'))(
            self,
            # BOOKMARK_DONE: join project command
            lambda formModal: self.join_project(formModal)
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

    def set_image(self, li, image):
        if image != None:
            photo = getdisplayableimage(image,(li.winfo_width(),205))
            li.lbl_image.configure(image=photo)
            li.lbl_image.image = photo

    def resize_image(self, event, li, image):
        self.set_image(li,image)

    # BOOKMARK_DONE: fill project items
    def fill_projects(self):
        # cleaning up old items
        self.lv_project.empty()
        # refilling 
        for item in Container.filter(Project, Project.ownerId == HomeWindow.ACTIVE_USER.id):
            if Container.filter(Session, Session.projectId == item.id).first() == None:
                li = self.lv_project.grid_item(item, {'title': item.title, 'creationDate': item.creationDate, 'lastEdited': item.lastEdited, 'image': item.image}, None, lambda i: self.create_list_item(i), 15)
                # self.set_image(li, item.image)
                li.lbl_image.bind('<Configure>', lambda e, l=li, image= item.image: self.resize_image(e, l, image))

    # BOOKMARK_DONE: fill session items
    def fill_sessions(self):
        # cleaning up old items
        self.lv_session.empty()
        # refilling 
        for item in Container.filter(Session):
            if item.owner == HomeWindow.ACTIVE_USER or Container.filter(Collaboration, Collaboration.userId == HomeWindow.ACTIVE_USER.id, Collaboration.sessionId == item.id).first() != None:
                li = self.lv_session.grid_item(item, {'title': item.title, 'creationDate': item.creationDate, 'lastEdited': item.project.lastEdited, 'memberCount': str(Container.filter(Collaboration,Collaboration.sessionId == item.id).count()+1), 'image': item.project.image}, None, lambda i: self.create_list_item(i, HomeWindow.SESSION_LI), 15)
                # self.set_image(li, item.project.image)
                li.lbl_image.bind('<Configure>', lambda e, l=li, image= item.project.image: self.resize_image(e, l, image))

    # BOOKMARK: Project List Item & Session List Item Creation Method
    def create_list_item(self, item: ListItem, liType: int = PROJECT_LI):
        item.configure (highlightthickness=1, highlightbackground=border, bg=white)
        comps = []

        img_size = 205
        img_thumb = Frame(item, height=img_size, bg=white)
        img_thumb.pack_propagate(0)

        # adding image label
        item.lbl_image = Label(img_thumb,bg='white')
        item.lbl_image.pack(fill=BOTH,expand=1)
        comps.append(item.lbl_image)

        border_bottom = Frame(item, bg=border)
        frm_info = Frame(item, bg=silver, padx=10, pady=10)
        frm_details = Frame(frm_info, bg=silver)
        
        lbl_title = Label(frm_info, text=item.bindings.get('title', '{title}'), bg=silver, fg=black, font='-size 18')
        lbl_title.pack(side=TOP, fill=X, pady=(0, 10))
        comps.append(lbl_title)

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
            comps.append(frm)
            lbl_label = Label(frm, text=i.get('label'), fg=teal, bg=silver, font='-size 8')
            lbl_label.pack(fill=X)
            comps.append(lbl_label)
            lbl_text = Label(frm, text=i.get('text'), fg=gray, bg=silver, font='-size 9')
            lbl_text.pack(fill=X)
            comps.append(lbl_text)

        
        img_thumb.pack(fill=X, side=TOP)
        comps.append(img_thumb)
        border_bottom.pack(fill=X, side=TOP)
        frm_info.pack(fill=X, side=TOP)
        comps.append(frm_info)
        frm_details.pack(fill=X, side=TOP)
        comps.append(frm_details)

        # BOOKMARK_DONE: project item's menu
        def options_menu(e):
            # convert screen mouse position
            win_coords = self.to_window_coords(e.x_root, e.y_root)
            menu_buttons = [
                {
                    'text': 'Open',
                    'icon': 'open.png',
                    'cmnd': lambda e: self.windowManager.run(ProjectWindow(self, item.dataObject)) if liType == HomeWindow.PROJECT_LI else self.windowManager.run(CollaborationWindow(self, item.dataObject))
                },
                {
                    'text': 'Edit',
                    'icon': 'edit.png',
                    'cmnd': lambda e: self.windowManager.run_tag('editor', item.dataObject)
                },
                {
                    'text': 'Share',
                    'icon': 'share.png',
                    'cmnd': lambda e: (self.windowManager.get_module('ShareModal'))(self, lambda modal: self.generate_share_link(item.dataObject, modal))
                },
                {
                    'text': 'Delete',
                    'icon': 'delete.png',
                    'fg': danger,
                    'cmnd': lambda e: self.delete_project(item.dataObject) if liType == self.PROJECT_LI else self.delete_session(item.dataObject) 
                },
                {
                    'text': 'Leave',
                    'icon': 'logout.png',
                    'fg': danger,
                    'cmnd': lambda e: self.quit_session(item.dataObject)
                }
            ]
            # pop unwanted buttons
            if liType == self.SESSION_LI: 
                # remove share button
                menu_buttons.pop(2)
                # remove delete or leave
                menu_buttons.pop(2 if item.dataObject.owner != HomeWindow.ACTIVE_USER else 3)
            else:
                # remove leave
                menu_buttons.pop()
            # show menu
            self.show_menu(x=win_coords[0], y=win_coords[1], width=150, height=200, options=menu_buttons)
        # options icon
        IconFrame(item, 'resources/icons/ui/menu.png', 10, teal, 32, options_menu, bg=white).place(relx=1-0.03, rely=0.02, anchor=N+E)

        for c in comps:
            c.bind('<Double-Button-1>', lambda e: self.windowManager.run(ProjectWindow(self, item.dataObject)) if liType == HomeWindow.PROJECT_LI else self.windowManager.run(CollaborationWindow(self, item.dataObject)))

    # BOOKMARK: this is how a COMMAND should be
    def create(self, modal, nature= PROJECT_LI, load= False):
        title = modal.get_form_data()['txt_title']
        date = datetime.now()

        def create_project(bytesFile= None):
            project = Project(title= title, creationDate= datetime.now(), lastEdited= datetime.now(), owner= HomeWindow.ACTIVE_USER, file= bytesFile)
            Container.save(project)
            self.lv_project.grid_item(project, {'title': project.title, 'creationDate': project.creationDate, 'lastEdited': project.lastEdited}, None, lambda i: self.create_list_item(i, HomeWindow.PROJECT_LI), 15)
            

        def create_session():
            project = Project(title= title+'Project', creationDate= date, lastEdited= date, owner= HomeWindow.ACTIVE_USER)
            session = Session(title= title, creationDate= date, owner= HomeWindow.ACTIVE_USER, project= project)
            Container.save(project, session)
            self.lv_session.grid_item(session, {'title': session.title, 'creationDate': project.creationDate, 'lastEdited': project.lastEdited, 'memberCount': str(Container.filter(Collaboration,Collaboration.sessionId == session.id).count()+1)}, None, lambda i: self.create_list_item(i, HomeWindow.SESSION_LI), 15)

        def load_project():
            title = modal.get_form_data()['txt_title']
            filename: str= modal.lbl_filename['text']
            if filename.endswith('...') != True and filename != '':
                create_project(filetobytes(filename))

        if not re.fullmatch('^[a-zA-Z0-9_]+( [a-zA-Z0-9_]+)*$', title):
            MessageModal(self,title=f'Title error',message=f'\n1. Must be between 4 - 20 characters \n2. should not contain any special character',messageType='error')
        else:
            create_session() if nature == HomeWindow.SESSION_LI else ( create_project() if load == False else load_project())
            modal.destroy()



    def delete(self, dataObject):
        Container.deleteObject(dataObject)
        self.clean_notifications()
        self.refresh_window()

    def delete_project(self, dataObject):
        MessageModal(self,title=f'Confirmation',message=f'Do you want to delete {dataObject.title} project?',messageType='prompt',actions={'yes' : lambda e: self.delete(dataObject)})

    def delete_session(self, dataObject):
        MessageModal(self,title=f'Confirmation',message=f'Do you want to delete {dataObject.title} session?',messageType='prompt',actions={'yes' : lambda e: self.delete(dataObject.project)})

    def quit_session(self, dataObject):
        MessageModal(self,title=f'Confirmation',message=f'Do you want to quit {dataObject.title} session?',messageType='prompt',actions={'yes' : lambda e: self.delete(Container.filter(Collaboration, Collaboration.userId == HomeWindow.ACTIVE_USER.id, Collaboration.sessionId == dataObject.id).first())})

    # BOOKMARK: this should redirect to the editor window
    def join_project(self, modal):
        link = modal.get_form_data()['txt_link']
        slink = Container.filter(ShareLink, ShareLink.link == link).first()
        if slink == None: MessageModal(self, title= f'Link error' ,message= 'This link doesn\'t exist!', messageType= 'error')
        elif slink.expirationDate < datetime.now(): MessageModal(self, title= f'Link error' ,message= 'This link has expired!', messageType= 'error')
        else:
            if slink.project.owner != HomeWindow.ACTIVE_USER :noti = Notification(notificationTime= datetime.now(), type= NotificationType.JOINED.value, nature= NotificationNature.SHARELINK.value, invitationId= slink.id, actor= HomeWindow.ACTIVE_USER, recipient= slink.project.owner)
            modal.destroy()
            self.windowManager.run(EditorWindow(self.master, slink.project))
            
    def join_session(self, modal):
        link = modal.get_form_data()['txt_link']
        date = datetime.now()
        invlink = Container.filter(InvitationLink, InvitationLink.link == link).first()
        if invlink == None: MessageModal(self, title= f'Link error' ,message= 'This link doesn\'t exist!', messageType= 'error')
        elif invlink.expirationDate < datetime.now(): MessageModal(self, title= f'Link error' ,message= 'This link has expired!', messageType= 'error')
        elif Container.filter(Collaboration, Collaboration.userId == HomeWindow.ACTIVE_USER.id, Collaboration.sessionId == invlink.sessionId).first() != None or invlink.session.owner == HomeWindow.ACTIVE_USER:
            MessageModal(self, title= f'Error' ,message= f'You are already in {invlink.session.title} session!', messageType= 'error')
        else:
            # create relations if they don't exist
            if Container.filter(Relation,Relation.userOne == HomeWindow.ACTIVE_USER, Relation.userTwo == invlink.sender ).first() == None: Container.save(Relation(userOne= HomeWindow.ACTIVE_USER, userTwo= invlink.sender))
            if Container.filter(Relation,Relation.userTwo == HomeWindow.ACTIVE_USER, Relation.userOne == invlink.sender ).first() == None: Container.save(Relation(userTwo= HomeWindow.ACTIVE_USER, userOne= invlink.sender))
            # create collaboration
            Container.save(Collaboration(joiningDate= date, privilege= invlink.privilege, user= HomeWindow.ACTIVE_USER, session= invlink.session))
            # add an acceptedInv type notification
            noti = Notification(notificationTime= date, type= NotificationType.JOINED.value, nature= NotificationNature.INVLINK.value, invitationId= invlink.id, actor= HomeWindow.ACTIVE_USER, recipient= invlink.sender)
            modal.destroy()
            self.windowManager.run(CollaborationWindow(self.master, invlink.session))


    def generate_share_link(self, dataObject, modal):
        def set_link(link):
            modal.form[0]['input'].entry.delete(0,END)
            modal.form[0]['input'].entry.insert(0,link)


        def check_privilege(msg, modal, slink):
            def generate_link(msg2, modal, slink, privilege):
                msg2.destroy()
                if slink != None: Container.deleteObject(slink)
                link= f'bpmntool//{dataObject.title}/{datetime.now()}/'
                Container.save(ShareLink(link=link, expirationDate=datetime.now()+timedelta(days=1), privilege= privilege, project=dataObject))
                self.clean_notifications()
                set_link(link)
            
            
            if msg != None: msg.destroy()
            msg2 = MessageModal(self,title=f'Confirmation',message=f'Do you want to grant this link the "edit" privilege?',messageType='prompt',actions={'yes' : lambda e: generate_link(msg2, modal, slink, 'edit'), 'no' : lambda e: generate_link(msg2, modal, slink, 'read')})

        def set_old_link(msg,modal):
            set_link(slink.link)
            msg.destroy()

        
        slink = Container.filter(ShareLink, ShareLink.projectId == dataObject.id).first()
        if slink != None:
            msg = check_privilege(None, modal, slink) if slink.expirationDate < datetime.now() else MessageModal(self,title='Link found',message=f'An active link already exists, Do you want to override it?',messageType='prompt',actions={'yes': lambda e: check_privilege(msg, modal, slink) , 'no': lambda e: set_old_link(msg,modal)})
        else:
            check_privilege(None, modal, None)

    def refresh_window(self, message=None):
        window = HomeWindow(self.master)
        self.windowManager.run(window)
        if message != None: MessageModal(window,title=f'Success',message=message,messageType='info')
        self.destroy()