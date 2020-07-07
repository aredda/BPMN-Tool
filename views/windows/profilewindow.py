from tkinter import *
from resources.colors import *
from views.windows.abstract.tabbedwindow import TabbedWindow
from views.components.listitem import ListItem
from views.components.icon import IconFrame
from views.factories.iconbuttonfactory import *
from views.components.scrollable import Scrollable
from views.components.textbox import TextBox

from models.entities.Container import Container
from models.entities.Entities import User,Relation

from helpers.imageutility import getdisplayableimage
from helpers.filehelper import filetobytes
import tkinter.filedialog as filedialog
import re
from views.windows.modals.messagemodal import MessageModal

class ProfileWindow(TabbedWindow):

    tabSettings = [
        {
            'tag': 'tb_info',
            'text': 'Profile',
            'icon': 'account.png'
        },
        {
            'tag': 'tb_collabs',
            'text': 'Saved Collaborators',
            'icon': 'session.png'
        }
    ]

    formSettings = [
        [
            {
                'label': 'First Name:',
                'icon': 'account.png',
                'tag': 'firstName'
            },
            {
                'label': 'Last Name:',
                'icon': 'account.png',
                'tag': 'lastName'
            },
            {
                'label': 'Username:',
                'icon': 'account.png',
                'tag': 'userName'
            },
            {
                'label': 'Email:',
                'icon': 'mail.png',
                'tag': 'email'
            }
        ],
        [
            {
                'label': 'Company:',
                'icon': 'business.png',
                'tag': 'company'
            },
            {
                'label': 'Gender:',
                'icon': 'wc.png',
                'tag': 'gender'
            },
            {
                'label': 'Password:',
                'icon': 'key.png',
                'tag': 'password'
            },
            {
                'label': 'Confirm Password:',
                'icon': 'key.png',
                'tag': 'confirmPwd'
            }
        ]
    ]

    def __init__(self, root, **args):
        TabbedWindow.__init__(self, root, ProfileWindow.tabSettings, 'Profile', **args)

        self.textBoxes = {}
        # self.image = {'bytes':ProfileWindow.ACTIVE_USER.image, 'label':None}
        self.lblimage = self.ACTIVE_USER.image

        self.collaboratorsItems = []

        self.design()
        self.fill_collaborators()
        self.fill_profile()
        self.get_form_data()

    def design(self):
        # Setup the tab of profile
        frm_form = Frame(self.tb_info, bg=background)
        frm_form.pack(fill=BOTH, expand=1)

        frm_form.rowconfigure(0, weight=1)
        frm_form.columnconfigure([0, 1, 2], weight=1)

        frm_image_column = Frame(frm_form, bg=background)
        frm_image_column.grid(row=0, column=0, padx=(0, 20))

        Label(frm_image_column, pady=10, bg=background, font='-size 10 -weight bold', fg=black, text='Profile Photo:', anchor=N+W).pack(side=TOP, fill=X)
        frm_image = Frame(frm_image_column, bg=black, height=150)
        frm_image.pack(side=TOP, fill=X, pady=(0, 10))

        self.lbl_image = Label(frm_image)
        
        # self.image['label'] = lbl_image
        self.set_image()

        SecondaryButton(frm_image_column, 'Upload Image', 'upload.png',btnCmd=lambda event: self.open_image(event)).pack (side=TOP, fill=X)

        for column in ProfileWindow.formSettings:
            # Prepare a form column
            frm_column = Frame(frm_form, bg=background)
            frm_column.grid(row=0, column=(1+ProfileWindow.formSettings.index(column)))
            # Loop through groups
            for group in column:
                # Prepare group
                frm_group = Frame(frm_column, bg=background)
                frm_group.pack(side=TOP, pady=10, padx=(0, 20))
                # Label and textbox
                Label(frm_group, bg=background, font='-size 10 -weight bold', fg=black, text=group.get('label'), anchor=N+W).pack(side=TOP, fill=X, pady=(0, 5))
                txt = TextBox(frm_group, 'resources/icons/ui/' + group.get('icon'))
                txt.pack(side=TOP)
                # Save the textbox in a list in order to get its value
                self.textBoxes[group.get('tag')] = txt

        frm_footer = Frame(self.tb_info, bg=background)
        frm_footer.pack(side=BOTTOM, fill=X)

        MainButton(frm_footer, 'Save Changes', 'save.png',btnCmd= lambda event: self.save_changes(event)).pack(side=LEFT)

        # Setup the tab of saved collabs
        frm_tip = IconButton(self.tb_collabs, 'Saved Collaborators are all the users who have participated in a collaboration session with you.', '-size 12 -weight bold', white, 'resources/icons/ui/info.png', 10, None, black, bg=black, pady=10, padx=5)
        frm_tip.pack(side=TOP, fill=X)

        self.lv_collabs = Scrollable(self.tb_collabs, bg=background, pady=20)
        self.lv_collabs.set_gridcols(2)
        self.lv_collabs.pack(expand=1, fill=BOTH)

    # BOOKMARK_DONE: this one is responsible for filling the scrollable container 
    def fill_collaborators(self):
        self.lv_collabs.empty()
        for i in Container.filter(Relation,Relation.userOneId == ProfileWindow.ACTIVE_USER.id):
            self.collaboratorsItems.append(
                self.lv_collabs.grid_item(i,
                {
                    'username':i.userTwo.userName,
                    'image':i.userTwo.image
                },
                [{'text': 'Remove', 'icon': 'cancel.png','cmd':lambda e, relation= i : self.remove_collaborator(relation)}], None, 15))

    # BOOKMARK_DONE: this method takes care of getting the data from the form in a form of dictionary
    def get_form_data(self):
        dic = {}

        for key,value in self.textBoxes.items():
            dic[key] = value.entry.get()
            # print(f'{key} : {value.entry.get()}')

        dic['image'] = self.lblimage
        return dic

    def fill_profile(self):
        for key,value in self.textBoxes.items():
            if hasattr(ProfileWindow.ACTIVE_USER, key) and getattr(ProfileWindow.ACTIVE_USER, key) != None:
                value.entry.insert(0, getattr(ProfileWindow.ACTIVE_USER, key))

    def open_image(self, event):
        self.lblimage = filetobytes(filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpeg/jpg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*"))))
        self.set_image()

    def set_image(self):  
        if self.lblimage != None:
            photo = getdisplayableimage(self.lblimage, (160,150))
            self.lbl_image.configure(image= photo)
            self.lbl_image.image = photo
            self.lbl_image.pack()

    def validate_form_data(self,data):
        validated = True

        def show_message(key,msg):
            MessageModal(self,title=f'{key} error',message=msg,messageType='error')
            return False

        for key, value in data.items():
            if key in ['firstName','lastName']:
                if not re.fullmatch('[A-Za-z]{2,15}( [A-Za-z]{2,15})?', value):
                    validated = show_message(key,f'\n1. can contain 2 words \n2. must be between 2 - 15 alphabets each \n3. can contain 1 space in the middle only \n4. should not contain any special characters or numbers')
                    break
            elif key in ['userName','password']:
                if not re.fullmatch('^(?=(?:[^a-z]*[a-z]))(?=[^A-Z]*[A-Z])(?=[^$@-]*[$@-])[a-zA-Z0-9$@-]{6,14}$', value):
                    validated = show_message(key,f'\n1. must be between 6 - 14 characters \n2. must contain 1 Capital letter \n3. must contain 1 special character ($@-)')
                    break
            elif key == 'email':
                if not re.fullmatch('[^@]+@[^@]+\.[^@]+', value):
                    validated = show_message(key,f'please enter a valid email ex: emailName@email.com')
                    break
            elif key == 'company':
                if value != '' and not re.fullmatch('[a-zA-Z0-9]{4,20}?', value):
                    validated = show_message(key,f'\n1. must be between 4 - 20 characters \n2. should contain alphabets and numbers only')
                    break
            elif key == 'gender':
                if value != '' and value.lower() not in ['female','male']:
                    validated = show_message(key,f'gender must be either male or female')
                    break
            elif key == 'confirmPwd':
                if value != data['password']:
                    validated = show_message(key,f'password doesn\'t match, please confirm your password')
                    break                   

        return validated


    def save_changes(self, event):
        data = self.get_form_data()
        if self.validate_form_data(data) == True:
            for key,value in self.textBoxes.items():
                if hasattr(ProfileWindow.ACTIVE_USER, key):
                    setattr(ProfileWindow.ACTIVE_USER,key,value.entry.get() if value.entry.get() != '' else None)
            ProfileWindow.ACTIVE_USER.image = self.lblimage
            Container.save(ProfileWindow.ACTIVE_USER)
            MessageModal(self,title=f'success',message='changes saved',messageType='info')
            self.windowManager.run(ProfileWindow(self.master))
            self.close()

    def remove_collaborator(self,relation):
        def delete_relation(relation):
            Container.deleteObject(relation)
            msg.destroy()
            for li in self.collaboratorsItems:
                if li.dataObject == relation: 
                    li.destroy()
                    self.collaboratorItems.remove(li)
            MessageModal(self,title=f'success',message='Collaborator removed',messageType='info')

        msg = MessageModal(self,title=f'confirmation',message=f'are you sure you want to remove {relation.userTwo.userName}',messageType='prompt',actions={'yes' : lambda e: delete_relation(relation)})

   