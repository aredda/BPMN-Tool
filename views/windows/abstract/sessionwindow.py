from tkinter import *
from resources.colors import *
from views.windows.abstract.window import Window
from views.components.iconbutton import IconButton
from views.components.icon import IconFrame
from views.factories.listitemfactory import ListItemFactory
from models.entities.Entities import Notification, Invitation, User
from models.entities.enums.notificationtype import NotificationType
import datetime

class SessionWindow(Window):

    # BOOKMARK: Signed in user
    ACTIVE_USER = None

    def __init__(self, root, title='Welcome', width=Window.DEFAULT_WIDTH, height=Window.DEFAULT_HEIGHT, **args):
        Window.__init__(self, root, title, width, height)

        self.frm_rSection = Frame(self, bg=background)
        self.frm_rSection.pack_propagate(0)
        
        self.frm_vBar = Frame(self, bg=black, padx=15, pady=15)
        self.frm_hBar = Frame(self.frm_rSection, bg=white, padx=20, pady=20)
        self.frm_hBarBorder = Frame(self.frm_rSection, height=1, bg=border)
        self.frm_body = Frame(self.frm_rSection, bg=background, padx=30, pady=30)

        self.frm_body.pack_propagate(0)
        self.frm_body.grid_propagate(0)

        self.frm_rSection.pack(side=RIGHT, fill=BOTH, expand=1)
        self.frm_vBar.pack(side=LEFT, fill=Y)
        self.frm_hBar.pack(side=TOP, fill=X)
        self.frm_hBarBorder.pack(side=TOP, fill=X)
        self.frm_body.pack(side=BOTTOM, expand=1, fill=BOTH)

        # vbar buttons
        self.vBarButtons = {}

        # Set up the bars
        self.config_vBar()
        self.config_hBar()

    def config_vBar(self):
        
        def callback(tag):
            return lambda e: self.windowManager.run_tag(tag)

        for i in SessionWindow.vBarSettings:
            # retrieve callable
            cb = callback(i.get('dest'))
            # instantiate button
            btn = IconButton(self.frm_vBar, i.get('text', 'Icon Button'), '-size 11 -weight bold', white, f'resources/icons/ui/{i["icon"]}', 0, None, black, 32, cb, bg=black, pady=10)
            btn.label.pack_forget()
            btn.pack(side=i.get('dock', TOP), fill=X)
            # save button
            self.vBarButtons[i.get('name')] = btn

        self.vBarButtons['btn_quit'].bind_click(lambda e: self.windowManager.quit())

    def config_hBar(self):
        # Creation of elements
        # BOOKMARK: change user profile image
        self.btn_username = IconButton(self.frm_hBar, 'Username', '-size 15', biege, 'resources/icons/ui/face.png', 5, None, biege, 40, None, bg=white)
        self.icn_notification = IconFrame(
            self.frm_hBar, 'resources/icons/ui/bell_outline.png', 0, None, 32,
            lambda e: self.show_popup(
                self.to_window_coords(e.x_root, e.y_root)[0] - 360, 
                self.to_window_coords(e.x_root, e.y_root)[1] + 20, 
                # BOOKMARK: notification data list
                [None, None, None], 
                ListItemFactory.NotificationListItem
            )
        )
        self.icn_discussion = IconFrame(
            self.frm_hBar, 'resources/icons/ui/discussion_outline.png', 0, None, 32,
            lambda e: self.show_popup(
                self.to_window_coords(e.x_root, e.y_root)[0] - 360, 
                self.to_window_coords(e.x_root, e.y_root)[1] + 20, 
                # BOOKMARK: discussion data list
                [None, None, None], 
                ListItemFactory.DiscussionListItem
            )
        )
        # Positioning elements
        self.btn_username.pack(side=LEFT)
        self.icn_notification.pack(side=RIGHT)
        self.icn_discussion.pack(side=RIGHT, padx=(0, 5))

    # Vertical Bar Settings
    vBarSettings = [
        {
            'name': 'btn_home',
            'icon': 'home.png',
            'text': 'Home',
            'dest': 'home'
        },
        {
            'name': 'btn_discussion',
            'icon': 'discussion_original.png',
            'text': 'Discussions',
            'dest': 'discussion'
        },
        {
            'name': 'btn_profile',
            'icon': 'settings.png',
            'text': 'Settings',
            'dest': 'profile'
        },
        {
            'name': 'btn_quit',
            'icon': 'logout.png',
            'text': 'Sign Out',
            'dest': None,
            'dock': BOTTOM
        }
    ]