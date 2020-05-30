from tkinter import *
from resources.colors import *
from views.windows.abstract.tabbedwindow import TabbedWindow
from views.components.listitem import ListItem
from views.components.icon import IconFrame
from views.components.iconbuttonfactory import *
from views.components.scrollable import Scrollable
from views.components.textbox import TextBox

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

        self.design()
        self.fill_collaborators()

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
        SecondaryButton(frm_image_column, 'Upload Image', 'upload.png').pack (side=TOP, fill=X)

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

        MainButton(frm_footer, 'Save Changes', 'save.png').pack(side=LEFT)

        # Setup the tab of saved collabs
        frm_tip = IconButton(self.tb_collabs, 'Saved Collaborators are all the users who have participated in a collaboration session with you.', '-size 12 -weight bold', white, 'resources/icons/ui/info.png', 10, None, black, bg=black, pady=10, padx=5)
        frm_tip.pack(side=TOP, fill=X)

        self.lv_collabs = Scrollable(self.tb_collabs, bg=background, pady=20)
        self.lv_collabs.set_gridcols(2)
        self.lv_collabs.pack(expand=1, fill=BOTH)

    # BOOKMARK: this one is responsible for filling the scrollable container 
    def fill_collaborators(self):
        self.lv_collabs.empty()
        for i in range(10):
            self.lv_collabs.grid_item(None, None, [{'text': 'Remove', 'icon': 'cancel.png'}], None, 15)

    # BOOKMARK: this method takes care of getting the date from the form in a form of dictionary
    def get_form_data(self):
        return {}