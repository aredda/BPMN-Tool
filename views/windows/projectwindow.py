from tkinter import *
from resources.colors import *
from views.windows.abstract.tabbedwindow import TabbedWindow
from views.components.listitem import ListItem
from views.components.icon import IconFrame
from views.factories.iconbuttonfactory import *
from views.components.scrollable import Scrollable

from models.entities.Container import Container
from models.entities.Entities import User, Project, History, ShareLink

import datetime

from views.windows.modals.messagemodal import MessageModal
import tkinter.filedialog as filedialog
from helpers.filehelper import bytestofile
from helpers.imageutility import getdisplayableimage
from views.windows.editorwindow import EditorWindow



class ProjectWindow(TabbedWindow):

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
        }
    ]

    def __init__(self, root, project=None, **args):
        TabbedWindow.__init__(self, root, ProjectWindow.tabSettings, project.title, **args)
        
        self.project = project
        self.configure_settings()

        self.historyItems = []

        # Button settings
        self.btnSettings = [
            {
                'icon': 'open.png',
                'text': 'Open Editor',
                'dock': LEFT,
                'cmnd': lambda e: self.windowManager.run(EditorWindow(self.master, self.project))
            },
            {
                'icon': 'share.png',
                'text': 'Share Project',
                'type': SecondaryButton,
                'cmnd': lambda e: (self.windowManager.get_module('ShareModal'))(
                    self,
                    # BOOKMARK_DONE: Share Project Command
                    lambda modal: self.generate_share_link(self.project, modal)
                )
            },
            {
                'icon': 'save.png',
                'text': 'Export as SVG'
            },
            {
                'icon': 'save.png',
                'text': 'Export as XML',
                'cmnd': lambda e: self.export_project('current_'+self.project.title, self.project.lastEdited, self.project.file)
            }
        ]

        # Design elements
        self.design()

    def get_btn_list(self, history):

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
                getattr(self, 'lbl_'+ ProjectWindow.lblSettings[2]['prop'])['text'] = history.editDate.strftime("%d/%m/%Y") if datetime.datetime.now().strftime("%x") != history.editDate.strftime("%x") else 'Today at - '+history.editDate.strftime("%X")
            
            msg = MessageModal(self,title=f'Confirmation',message=f'Are you sure you want to revert to that change?',messageType='prompt',actions={'yes' : lambda e: revert_changes(msg,history)})

        btns = [
                {
                    'icon': 'save.png',
                    'text': 'Export to XML',
                    'cmd': lambda e: self.export_project(history.project.title, history.editDate, history.file)
                },
                {
                    'icon': 'revert_history.png',
                    'text': 'Revert',
                    'cmd': lambda e: ask_revert_changes(history)
                }
            ] 

        return btns

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

        for i in ProjectWindow.lblSettings:
            frm_lbl_group = Frame(frm_label_container, bg=background)
            frm_lbl_group.pack(side=LEFT, fill=X, expand=1)
            
            lbl_label = Label(frm_lbl_group, bg=background, fg=teal,  font='-size 16', text=i.get('label'), anchor='nw')
            lbl_label.pack(side=TOP, fill=X)
            
            lbl_prop = Label(frm_lbl_group, bg=background, fg=black, font='-size 13', text=i.get('prop'), anchor='nw')
            lbl_prop.pack(side=TOP, fill=X)

            setattr(self, 'lbl_' + i.get('prop'), lbl_prop)

        frm_preview = Frame(self.tb_info, bg=white, highlightthickness=1, highlightbackground=border)
        frm_preview.pack(expand=1, fill=BOTH, pady=15)

        frm_preview.update()

        if self.project.image != None:
            photo = getdisplayableimage(self.project.image,(self.tb_info.winfo_width(),self.tb_info.winfo_height()))
            lbl_image = Label(frm_preview, image = photo)
            lbl_image.image=photo
            lbl_image.pack(fill=BOTH,expand=1)


        # Filling the history tab
        self.frm_list_view = Scrollable(self.tb_hist, bg=background)
        self.frm_list_view.pack(expand=1, fill=BOTH, pady=(0, 15))

        # BOOKMARK: fill history items
        for i in Container.filter(History, History.projectId == self.project.id).order_by(History.editDate.desc()):
            li = ListItem(self.frm_list_view.interior, i, {'username': f'{i.editor.userName} edited on {i.editDate.strftime("%d/%m/%Y at %X")}', 'image': i.editor.image}, self.get_btn_list(i))
            li.pack(anchor=N+W, pady=(0, 10), fill=X, padx=5)
            self.historyItems.append(li)
    
    def configure_settings(self):
        ProjectWindow.lblSettings[0]['prop'] = self.project.title 
        ProjectWindow.lblSettings[1]['prop'] = self.project.creationDate.strftime("%d/%m/%Y") if datetime.datetime.now().strftime("%x") != self.project.creationDate.strftime("%x") else 'Today at - '+self.project.creationDate.strftime("%X")
        ProjectWindow.lblSettings[2]['prop'] = self.project.lastEdited.strftime("%d/%m/%Y") if datetime.datetime.now().strftime("%x") != self.project.lastEdited.strftime("%x") else 'Today at - '+self.project.lastEdited.strftime("%X")

    def export_project(self, title, date, fileBytes):
        if fileBytes == None:
            MessageModal(self, title= 'Error', message= 'No changes has been made on this project!', messageType= 'error')
        else:    
            folderName = filedialog.askdirectory(initialdir="/", title='Please select a directory')

            if folderName != '':
                bytestofile(f'{folderName}',f'{title}_{date.strftime("%d-%m-%Y_%H-%M-%S")}','xml',fileBytes)
                MessageModal(self,title=f'Success',message=f'File saved in {folderName}!',messageType='info')

    def generate_share_link(self, dataObject, modal):
        def set_link(link):
            modal.form[0]['input'].entry.delete(0,END)
            modal.form[0]['input'].entry.insert(0,link)


        def check_privilege(msg, modal, slink):
            def generate_link(msg2, modal, slink, privilege):
                msg2.destroy()
                if slink != None: Container.deleteObject(slink)
                link= f'bpmntool//{dataObject.title}/{datetime.datetime.now()}/'
                Container.save(ShareLink(link=link, expirationDate=datetime.datetime.now()+datetime.timedelta(days=1), privilege= privilege, project=dataObject))
                self.clean_notifications()
                set_link(link)
            
            
            if msg != None: msg.destroy()
            msg2 = MessageModal(self,title=f'Confirmation',message=f'Do you want to grant this link the "edit" privilege?',messageType='prompt',actions={'yes' : lambda e: generate_link(msg2, modal, slink, 'edit'), 'no' : lambda e: generate_link(msg2, modal, slink, 'read')})

        def set_old_link(msg,modal):
            set_link(slink.link)
            msg.destroy()

        
        slink = Container.filter(ShareLink, ShareLink.projectId == dataObject.id).first()
        if slink != None:
            msg = check_privilege(None, modal, slink) if slink.expirationDate < datetime.datetime.now() else MessageModal(self,title='Link found',message=f'A link already exists, Do you want to override it?',messageType='prompt',actions={'yes': lambda e: check_privilege(msg, modal, slink) , 'no': lambda e: set_old_link(msg,modal)})
        else:
            check_privilege(None, modal, None)