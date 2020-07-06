from tkinter import *
from resources.colors import *
from views.windows.abstract.tabbedwindow import TabbedWindow
from views.components.listitem import ListItem
from views.components.icon import IconFrame
from views.factories.iconbuttonfactory import *
from views.components.scrollable import Scrollable

from models.entities.Container import Container
from models.entities.Entities import Collaboration,User,History
from sqlalchemy import or_,func
import datetime
from helpers.imageutility import getdisplayableimage
from views.windows.modals.messagemodal import MessageModal

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
        self.configure_settings(session)

        self.collaboratorItems = []
        self.historyItems = []

        # configure button settings
        self.btnSettings = [
            {
                'icon': 'open.png',
                'text': 'Open Editor',
                'dock': LEFT
            },
            {
                'icon': 'delete.png',
                'text': 'End Session',
                'type': DangerButton,
                # BOOKARK: Ending Session Command
                'cmnd': lambda e: self.show_prompt('Are you really sure to terminate the session?', lambda e: print ('termination logic'), 'Terminating the session')
            },
            {
                'icon': 'invite.png',
                'text': 'Invite',
                'type': SecondaryButton,
                'cmnd': lambda e: (self.windowManager.get_module('InviteModal'))(
                    self,
                    # BOOKMARK: Activate Link Command
                    lambda modal: print(modal.get_form_data()),
                    # BOOKMARK: Invite User Command
                    lambda modal: print(modal.get_form_data())
                )
            },
            {
                'icon': 'save.png',
                'text': 'Export as SVG',
                'dock': LEFT
            },
            {
                'icon': 'save.png',
                'text': 'Export as XML',
                'dock': LEFT
            }
        ]

        if CollaborationWindow.ACTIVE_USER != self.session.owner:
            self.btnSettings.pop(1) 

        # Design elements
        self.design()
        # Fill session members
        self.fill_members()
    
    def configure_settings(self,session):
        CollaborationWindow.lblSettings[0]['prop'] = session.project.title
        CollaborationWindow.lblSettings[1]['prop'] = self.session.creationDate.strftime("%d/%m/%Y") if datetime.datetime.now().strftime("%x") != self.session.creationDate.strftime("%x") else 'Today at - '+self.session.creationDate.strftime("%X")
        CollaborationWindow.lblSettings[2]['prop'] = self.session.project.lastEdited.strftime("%d/%m/%Y") if datetime.datetime.now().strftime("%x") != self.session.project.lastEdited.strftime("%x") else 'Today at - '+self.session.project.lastEdited.strftime("%X")
        CollaborationWindow.lblSettings[3]['prop'] = str(Container.filter(Collaboration,Collaboration.sessionId == session.id).count()+1)

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

        frm_preview = Frame(frm_group, bg=white, highlightthickness=1, highlightbackground=border)

        if self.session.project.image != None:
            photo = getdisplayableimage(self.session.project.image,(600,600))
            lbl_image = Label(frm_preview, image = photo)
            lbl_image.image=photo
            lbl_image.pack(fill=BOTH,expand=1)

        frm_preview.pack(side=LEFT, fill=BOTH, expand=1)

        self.lv_members = Scrollable(frm_group, bg=background)
        self.lv_members.pack(side=RIGHT, fill=BOTH, padx=(10, 0))

        # Filling the history tab
        self.frm_list_view = Scrollable(self.tb_hist, bg=background)
        self.frm_list_view.pack(expand=1, fill=BOTH, pady=(0, 15))

        # BOOKMARK_DONE: Fill Collaboration Session Change History
        for i in Container.filter(History, History.projectId == self.session.projectId, self.session.id == Collaboration.sessionId).order_by(History.editDate.desc()).all():#, or_(History.editorId == Collaboration.userId, History.editorId == self.session.ownerId) since the project is gonna be unique
            li = ListItem(self.frm_list_view.interior, i,
                {
                    'username': f'{i.editor.userName} edited on {i.editDate.strftime("%d/%m/%Y at %X")}'
                },
                self.get_btn_list(i))
            li.pack(anchor=N+W, fill=X, pady=(0, 10), padx=5)
            self.historyItems.append(li)

    def get_btn_list(self,history):
          
        def ask_revert_changes(history):
            def revert_changes(msg,history):
                history.project.file = history.file
                history.project.lastEdited = history.editDate
                Container.save(history.project)
                msg.destroy()

                for li in self.historyItems:
                    if li.dataObject.editDate > history.editDate and li.dataObject.id != history.id: 
                        Container.deleteObject(li.dataObject)
                        li.destroy()
                
                MessageModal(self,title=f'success',message=f'changes reverted',messageType='info')
                getattr(self, 'lbl_'+ CollaborationWindow.lblSettings[2]['prop'])['text'] = history.editDate.strftime("%d/%m/%Y") if datetime.datetime.now().strftime("%x") != history.editDate.strftime("%x") else 'Today at - '+history.editDate.strftime("%X")
            
            msg = MessageModal(self,title=f'confirmation',message=f'are you sure you want to revert to that change ?',messageType='prompt',actions={'yes' : lambda e: revert_changes(msg,history)})

        

        btn_list = [{
                    'icon': 'save.png',
                    'text': 'Export to XML'
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
                    'username' : i.userName
                },
                [{
                    'icon': 'cancel.png',
                    'text': 'Kick',
                    'cmd' : lambda e, user= i: self.kick_user(user), 

                }] if CollaborationWindow.ACTIVE_USER == self.session.owner else None
                )
            li.pack(anchor=N+W, pady=(0, 10), padx=(0, 10))
            self.collaboratorItems.append(li)
            

    def kick_user(self, user):
        def delete_collaboration(user):
            Container.deleteObject(Container.filter(Collaboration,Collaboration.userId == user.id , Collaboration.sessionId == self.session.id).first())
            msg.destroy()
            for li in self.collaboratorItems:
                if li.dataObject == user: 
                    li.destroy()
                    getattr(self, 'lbl_'+ CollaborationWindow.lblSettings[3]['prop'])['text'] = str(Container.filter(Collaboration,Collaboration.sessionId == self.session.id).count()+1)
                    
            MessageModal(self,title=f'success',message=f'collaborator kicked',messageType='info')


        msg = MessageModal(self,title=f'confirmation',message=f'are you sure you want to kick {user.userName}',messageType='prompt',actions={'yes' : lambda e: delete_collaboration(user)})

        