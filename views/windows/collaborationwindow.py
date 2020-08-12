from tkinter import *
from resources.colors import *
from views.windows.abstract.tabbedwindow import TabbedWindow
from views.components.listitem import ListItem
from views.components.icon import IconFrame
from views.factories.iconbuttonfactory import *
from views.components.scrollable import Scrollable

from models.entities.Container import Container
from models.entities.Entities import Collaboration,User,History,Invitation,InvitationLink,Notification
from models.entities.enums.notificationnature import NotificationNature
from models.entities.enums.notificationtype import NotificationType
from models.entities.enums.status import Status
from sqlalchemy import or_,func
import datetime
from helpers.imageutility import getdisplayableimage
from helpers.filehelper import bytestofile
from views.windows.modals.messagemodal import MessageModal
import tkinter.filedialog as filedialog
from views.windows.editorwindow import EditorWindow


class CollaborationWindow(TabbedWindow):

    tabSettings = [
        {   
            'icon': 'info.png',
            'text': 'General Info',
            'tag': 'tb_info'
        },
        {   
            'icon': 'history.png',
            'text': 'History',
            'tag': 'tb_hist'
        },
        {
            'icon': 'session.png',
            'text': 'Members',
            'tag': 'tb_member'
        }
    ]

    lblSettings = [
        {
            'label': 'Project\'s Title:',
            'prop': 'title'
        },
        {
            'label': 'Creation Date:',
            'prop': 'creationDate'
        },
        {
            'label': 'Last Edit:',
            'prop': 'lastEdit'
        },
        {
            'label': 'Members:',
            'prop': 'memberCount'
        }
    ]

    def __init__(self, root, session=None, **args):
        TabbedWindow.__init__(self, root, CollaborationWindow.tabSettings, session.title, **args)

        self.session = session

        self.collaboratorItems = []
        self.historyItems = []

        # configure button settings
        self.btnSettings = [
            {
                'icon': 'open.png',
                'text': 'Open Editor',
                'dock': LEFT,
                'cmnd': lambda e: self.windowManager.run(EditorWindow(self.master, self.session))
            },
            {
                'icon': 'delete.png',
                'text': 'End Session',
                'type': DangerButton,
                # BOOKARK: Ending Session Command
                'cmnd': lambda e: self.show_prompt('Are you sure you want to terminate the session?', lambda e: self.delete_session(), 'Terminating the session')
            },
            {
                'icon': 'invite.png',
                'text': 'Invite',
                'type': SecondaryButton,
                'cmnd': lambda e: (self.windowManager.get_module('InviteModal'))(
                    self,
                    # BOOKMARK_DONE: Activate Link Command
                    lambda modal: self.generate_inviationlink(modal),# modal.get_form_data()['txt_link']
                    # BOOKMARK_DONE: Invite User Command
                    lambda modal: self.invite_user(modal.get_form_data()['txt_username'])
                )
            },
            {
                'icon': 'save.png',
                'text': 'Export as XML',
                'dock': LEFT,
                'cmnd': lambda e: self.export_project(f'current_{self.session.project.title}',self.session.project.lastEdited,self.session.project.file)
            }
        ]

        if CollaborationWindow.ACTIVE_USER != self.session.owner:
            self.btnSettings.pop(1) 

        # Design elements
        self.design()
        # Fill session members
        self.fill_members()

    def generate_inviationlink(self, modal):
        # modal.form[0]['input'].entry.get()
        def set_link(link):
            modal.form[0]['input'].entry.delete(0,END)
            modal.form[0]['input'].entry.insert(0,link)


        def check_privilege(msg, modal, inv):
            def generate_link(msg2, modal, inv, privilege):
                msg2.destroy()
                if inv != None: Container.deleteObject(inv)
                link= f'bpmntool//{self.session.title}/{datetime.datetime.now()}/'
                Container.save(InvitationLink(link=link, expirationDate=datetime.datetime.now()+datetime.timedelta(days=1), privilege= privilege, sender=CollaborationWindow.ACTIVE_USER, session=self.session))
                self.clean_notifications()
                set_link(link)
            
            
            if msg != None: msg.destroy()
            msg2 = MessageModal(self,title=f'Confirmation',message=f'Do you want to grant this link the "edit" privilege?',messageType='prompt',actions={'yes' : lambda e: generate_link(msg2, modal, inv, 'edit'), 'no' : lambda e: generate_link(msg2, modal, inv, 'read')})

        def set_old_link(msg,modal):
            set_link(inv.link)
            msg.destroy()

        inv = Container.filter(InvitationLink, InvitationLink.senderId == CollaborationWindow.ACTIVE_USER.id, InvitationLink.sessionId == self.session.id).first()
        if inv != None:
            msg = check_privilege(None, modal, inv) if inv.expirationDate < datetime.datetime.now() else MessageModal(self,title='link found',message=f'A link already exists, Do you want to override it?',messageType='prompt',actions={'yes': lambda e: check_privilege(msg, modal, inv) , 'no': lambda e: set_old_link(msg,modal)})
        else:
            check_privilege(None, modal, None)

    def invite_user(self, username):
        def send_invite(msg, user, privilege):
            inv = Invitation(privilege= privilege, invitationTime= datetime.datetime.now(), sender=CollaborationWindow.ACTIVE_USER, recipient= user, session= self.session)
            Container.save(inv)
            notif =  Notification(type= NotificationType.INVITED.value, notificationTime= datetime.datetime.now(), nature= NotificationNature.INV.value, invitationId= inv.id, actor= inv.sender, recipient= inv.recipient)
            Container.save(notif)
            msg.destroy()
            MessageModal(self,title=f'Success',message=f'Invitation sent to {user.userName} successfully!',messageType='info')


        user = Container.filter(User, User.userName == username).first()
        collabs = Container.filter(User, Collaboration.sessionId == self.session.id,or_(User.id == Collaboration.userId,User.id == self.session.ownerId)).all()
        
        if user == None:
            MessageModal(self,title='User error 404',message=f'{username} doesn\'t exist!' if username != '' and not str.isspace(username) else 'Please enter a username!',messageType='error')
        elif user in collabs:
            MessageModal(self,title='User already in',message=f'{username} is already in the session!',messageType='error')
        elif Container.filter(Invitation, Invitation.recipientId == user.id, Invitation.sessionId == self.session.id, Invitation.status == Status.PENDING.value).first() != None:
            MessageModal(self,title='User already invited',message=f'An invite is already sent to {username}!',messageType='info')
        else:
            msg = MessageModal(self,title=f'Confirmation',message=f'Do you want to give {username} the right to make changes?',messageType='prompt',actions={'yes' : lambda e: send_invite(msg,user,'edit'), 'no' : lambda e: send_invite(msg,user,'read')})

    def delete_session(self):
        Container.deleteObject(self.session.project)
        self.clean_notifications()
        self.windowManager.run_tag('home')
        self.destroy()
    
    def configure_settings(self):
        # 
        get_label = lambda prop: getattr(self, f'lbl_{prop}')
        # change label
        get_label(CollaborationWindow.lblSettings[0]['prop'])['text'] = self.session.project.title
        get_label(CollaborationWindow.lblSettings[1]['prop'])['text'] = self.session.creationDate.strftime("%d/%m/%Y") if datetime.datetime.now().strftime("%x") != self.session.creationDate.strftime("%x") else 'Today at - '+self.session.creationDate.strftime("%X")
        get_label(CollaborationWindow.lblSettings[2]['prop'])['text'] = self.session.project.lastEdited.strftime("%d/%m/%Y") if datetime.datetime.now().strftime("%x") != self.session.project.lastEdited.strftime("%x") else 'Today at - '+self.session.project.lastEdited.strftime("%X")
        get_label(CollaborationWindow.lblSettings[3]['prop'])['text'] = str(Container.filter(Collaboration,Collaboration.sessionId == self.session.id).count()+1)
        # change image
        if self.session.project.image !=None:
            photo = getdisplayableimage(self.session.project.image, (self.frm_preview.winfo_width(), self.frm_preview.winfo_height()))
            self.lbl_image.configure (image=photo)
            self.lbl_image.image = photo
        # fill
        self.fill_collaboration()
        self.fill_members()

    def design(self):
        # Putting the control buttons
        btn_container = Frame(self.frm_body, bg=background)
        btn_container.pack(fill=X, side=TOP)

        for i in self.btnSettings:
            childCount = len (btn_container.pack_slaves())
            method = i.get('type', MainButton)
            btn = method(btn_container, i.get('text', 'Button'), i.get('icon', 'error.png'), i.get('cmnd', None))
            btn.pack(side=i.get('dock', RIGHT), padx=(0 if childCount == 0 else 10, 0))
        
        # Filling the information tab
        frm_label_container = Frame(self.tb_info, bg=black)
        frm_label_container.pack(side=TOP, fill=X)

        for i in CollaborationWindow.lblSettings:
            frm_lbl_group = Frame(frm_label_container, bg=background)
            frm_lbl_group.pack(side=LEFT, fill=X, expand=1)
            
            lbl_label = Label(frm_lbl_group, bg=background, fg=teal,  font='-size 16', text=i.get('label'), anchor='nw')
            lbl_label.pack(side=TOP, fill=X)
            
            lbl_prop = Label(frm_lbl_group, bg=background, fg=black, font='-size 13', text=i.get('prop'), anchor='nw')
            lbl_prop.pack(side=TOP, fill=X)

            setattr(self, 'lbl_' + i.get('prop'), lbl_prop)

        frm_group = Frame(self.tb_info, bg=background)
        frm_group.pack(expand=1, fill=BOTH, pady=15)

        self.frm_preview = Frame(frm_group, bg=white, highlightthickness=1, highlightbackground=border)
        self.frm_preview.pack(side=LEFT, fill=BOTH, expand=1)

        self.frm_preview.update()

        def resize_image(event, label):
            if self.session.project.image !=None:
                photo = getdisplayableimage(self.session.project.image, (self.frm_preview.winfo_width(), self.frm_preview.winfo_height()))
                label.configure(image=photo)
                label.image = photo

        self.lbl_image = Label(self.frm_preview, bg='white')
        self.lbl_image.pack(fill=BOTH, expand=1)
        self.lbl_image.bind('<Configure>', lambda e, l=self.lbl_image: resize_image(e, l))

        # Filling the history tab
        self.frm_list_view = Scrollable(self.tb_hist, bg=background)
        self.frm_list_view.pack(expand=1, fill=BOTH, pady=(0, 15))

        # filling member tab
        self.lv_members = Scrollable(self.tb_member, bg=background)
        self.lv_members.pack(fill=BOTH, expand=1)

        self.fill_collaboration()

    def fill_collaboration(self):
        self.frm_list_view.empty()
        # BOOKMARK_DONE: Fill Collaboration Session Change History
        for i in Container.filter(History, History.projectId == self.session.projectId).order_by(History.editDate.desc()).all():#, or_(History.editorId == Collaboration.userId, History.editorId == self.session.ownerId) since the project is gonna be unique
            if i.project.owner == CollaborationWindow.ACTIVE_USER or Container.filter(Collaboration, Collaboration.sessionId == self.session.id, Collaboration.userId == CollaborationWindow.ACTIVE_USER.id).first() != None:
                li = ListItem(self.frm_list_view.interior, i,
                    {
                        'username': f'{i.editor.userName} edited on {i.editDate.strftime("%d/%m/%Y at %X")}',
                        'image': i.editor.image
                    },
                    self.get_btn_list(i))
                li.pack(anchor=N+W, fill=X, pady=(0, 10), padx=5)
                self.historyItems.append(li)

    def export_project(self, title, date, fileBytes):
        if fileBytes == None:
            MessageModal(self, title= 'Error', message= 'No changes has been made yet on this session\'s project yet!', messageType= 'error')
        else: 
            folderName = filedialog.askdirectory(initialdir="/", title='Please select a directory')

            if folderName != '':
                bytestofile(f'{folderName}',f'{title}_{date.strftime("%d-%m-%Y_%H-%M-%S")}','xml',fileBytes)
                MessageModal(self,title=f'Success',message=f'File saved in {folderName}!',messageType='info')
    
    def get_btn_list(self,history):
        
        def ask_revert_changes(history):
            def revert_changes(msg,history):
                history.project.file = history.file
                history.project.lastEdited = history.editDate
                Container.save(history.project)
                msg.destroy()

                for li in self.historyItems:
                    if li.dataObject.editDate >= history.editDate: 
                        Container.deleteObject(li.dataObject)
                        li.destroy()
                
                MessageModal(self,title=f'Success',message=f'Changes reverted to the following date:\n{history.editDate.strftime("%x - %X")}!',messageType='info')
                getattr(self, 'lbl_'+ CollaborationWindow.lblSettings[2]['prop'])['text'] = history.editDate.strftime("%d/%m/%Y") if datetime.datetime.now().strftime("%x") != history.editDate.strftime("%x") else 'Today at - '+history.editDate.strftime("%X")
            
            msg = MessageModal(self,title=f'Confirmation',message=f'Are you sure you want to revert to that change?',messageType='prompt',actions={'yes' : lambda e: revert_changes(msg,history)})


        btn_list = [{
                    'icon': 'save.png',
                    'text': 'Export to XML',
                    'cmd': lambda e: self.export_project(history.project.title, history.editDate,history.file)
                },
                {
                    'icon': 'revert_history.png',
                    'text': 'Revert',
                    'cmd': lambda e: ask_revert_changes(history)
                }]

        if CollaborationWindow.ACTIVE_USER != self.session.owner:
            btn_list.pop(1)

        return btn_list

    # BOOKMARK_DONE: Fill Collaboration Session Members
    def fill_members(self):
        # Remove all items
        self.lv_members.empty()
        # Append items
        for i in Container.filter(User, Collaboration.sessionId == self.session.id,User.id != CollaborationWindow.ACTIVE_USER.id,or_(User.id == Collaboration.userId,User.id == self.session.ownerId)).all():
            li = ListItem(self.lv_members.interior, i, 
                {
                    'username' : i.userName,
                    'image': i.image
                },
                [{
                    'icon': 'cancel.png',
                    'text': 'Kick',
                    'cmd' : lambda e, user= i: self.kick_user(user), 

                }] if CollaborationWindow.ACTIVE_USER == self.session.owner else None
                )
            li.pack(anchor=N+W, pady=(0, 10), padx=(0, 10), fill=X)
            self.collaboratorItems.append(li)

    def kick_user(self, user):
        def delete_collaboration(user):
            Container.deleteObject(Container.filter(Collaboration,Collaboration.userId == user.id , Collaboration.sessionId == self.session.id).first())
            msg.destroy()
            for li in self.collaboratorItems:
                if li.dataObject == user: 
                    li.destroy()
                    getattr(self, 'lbl_'+ CollaborationWindow.lblSettings[3]['prop'])['text'] = str(Container.filter(Collaboration,Collaboration.sessionId == self.session.id).count()+1)
                    
            MessageModal(self,title=f'Success',message=f'{user.userName} has been kicked out of the session!',messageType='info')

        msg = MessageModal(self,title=f'Confirmation',message=f'Are you sure you want to kick {user.userName}?',messageType='prompt',actions={'yes' : lambda e: delete_collaboration(user)})

    def refresh(self):
        super().refresh()

        self.configure_settings()