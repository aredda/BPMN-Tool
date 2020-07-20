from tkinter import *
from resources.colors import *
from views.windows.abstract.window import Window
from views.components.iconbutton import IconButton
from views.components.icon import IconFrame
from views.factories.listitemfactory import ListItemFactory
from models.entities.Entities import Notification, Invitation, User,Collaboration,Session,Message, SeenNotification, SeenMessage, InvitationLink, ShareLink
from models.entities.enums.notificationtype import NotificationType
from models.entities.enums.notificationnature import NotificationNature
import datetime

from models.entities.Container import Container
from sqlalchemy import and_,or_,func

import time
import threading

from PIL import Image as Img, ImageTk as ImgTk

class SessionWindow(Window):

    # Chat Session Item Styles
    CHAT_NORMAL = {
        'bg': white,
        'lbl_username': teal,
        'lbl_content': black,
        'lbl_time': gray 
    }
    CHAT_UNREAD = {
        'bg': background,
        'lbl_username': teal,
        'lbl_content': black,
        'lbl_time': gray 
    }

    # BOOKMARK_UNDONE: Signed in user
    ACTIVE_USER = Container.filter(User).get(2)

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


    def runnable(self):
        try:
            while self.time_to_kill != True:
                Container.session.begin()
                Container.session.commit()
                noNewNotifs = True
                noNewMessages = True
                # check for new unseen notifications
                for notif in Container.filter(Notification,Notification.recipient == SessionWindow.ACTIVE_USER, Notification.id.notin_(Container.filter(SeenNotification.notificationId.distinct()))).all():
                    if Container.filter(SeenNotification, SeenNotification.notificationId == notif.id, SeenNotification.seerId == SessionWindow.ACTIVE_USER.id).first() == None: 
                        self.icn_notification.set_image('resources/icons/ui/bell_ring.png')
                        noNewNotifs = False
                        break
                # check for new unseen messages
                for msg in Container.filter(Message,Message.sessionId == Collaboration.sessionId,or_(Collaboration.userId == SessionWindow.ACTIVE_USER.id, and_(Message.sessionId == Session.id, Session.ownerId == SessionWindow.ACTIVE_USER.id) ),Message.sentDate.in_(Container.filter(func.max(Message.sentDate)).group_by(Message.sessionId))).group_by(Message.sessionId).all():
                    if msg.user != SessionWindow.ACTIVE_USER and Container.filter(SeenMessage, SeenMessage.messageId == msg.id).first() == None:
                        self.icn_discussion.set_image('resources/icons/ui/discussion.png')
                        noNewMessages = False
                        break
                # change the icon if there is no new notifications
                if noNewNotifs: self.icn_notification.set_image('resources/icons/ui/bell_outline.png')
                # change the icon if there is no new messages
                if noNewMessages: self.icn_discussion.set_image('resources/icons/ui/discussion_outline.png')
                time.sleep(2)
        except Exception:
            # Container.session.rollback()
            print('RUNNABLE1 ERROR')
        
    def hide(self):
        # thread killer logic will be here
        self.time_to_kill = True
        # continute the original work
        super().hide()

    def refresh(self): # this should run 
        self.time_to_kill = False
        # start thread
        threading.Thread(target=self.runnable).start()


    def change_session_item_style(self, item, style=CHAT_UNREAD):
        # Change background
        changeBgTo = [item, item.frm_content, item.lbl_username, item.lbl_content, item.lbl_time, item.img_photo]
        for w in changeBgTo:
            w.config(bg=style['bg'])
        # Change foreground
        for i in style.keys():
            if hasattr(item, i):
                getattr(item, i).config(fg=style[i])


    def configure_msg_listitem(self, root, item):
        li = ListItemFactory.DiscussionListItem(root, item)
        # set message listItem click
        comps = [li, li.frm_content, li.lbl_username, li.lbl_content, li.lbl_time, li.img_photo]
        for c in comps:
            c.bind('<Button-1>', lambda e: self.windowManager.run_tag('discussion',session= item.session))
        # change style for unread messages
        if item.user != self.ACTIVE_USER and Container.filter(SeenMessage, SeenMessage.messageId == item.id,SeenMessage.seerId == SessionWindow.ACTIVE_USER.id).first() == None:
                self.change_session_item_style(li,self.CHAT_UNREAD)
        # change message icon's image on click
        self.icn_discussion.set_image('resources/icons/ui/discussion_outline.png')
        return li

    def configure_notif_listitem(self, root, item):
        li= ListItemFactory.NotificationListItem(root, item)
        # save notification that are not recieveInv as seen 
        if item.type != NotificationType.INVITED.value and Container.filter(SeenNotification, SeenNotification.notificationId == item.id, SeenNotification.seerId == SessionWindow.ACTIVE_USER.id).first() == None: 
                Container.save(SeenNotification(date= datetime.datetime.now(), seer= SessionWindow.ACTIVE_USER, notification= item))
         # change notification icon's image on click
        self.icn_notification.set_image('resources/icons/ui/bell_outline.png')
        return li

    def clean_notifications(self):
        notifs = Container.filter(Notification)
        for notif in notifs:
            if notif.nature == NotificationNature.INV.value and Container.filter(Invitation, Invitation.id == notif.invitationId).first() == None:
                Container.deleteObject(notif)
            elif notif.nature == NotificationNature.INVLINK.value and Container.filter(InvitationLink, InvitationLink.id == notif.invitationId).first() == None:
                Container.deleteObject(notif)
            elif notif.nature == NotificationNature.SHARELINK.value and Container.filter(ShareLink, ShareLink.id == notif.invitationId).first() == None:
                Container.deleteObject(notif)

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

        def quit():
            self.time_to_kill = True
            self.windowManager.quit()

        self.vBarButtons['btn_quit'].bind_click(lambda e: quit() )


    def config_hBar(self):
        # Creation of elements
        # BOOKMARK_DONE: change user profile image
        self.btn_username = IconButton(self.frm_hBar, SessionWindow.ACTIVE_USER.userName, '-size 15', biege, 'resources/icons/ui/face.png' if SessionWindow.ACTIVE_USER.image == None else SessionWindow.ACTIVE_USER.image, 5, None, biege, 40, None, bg=white)
        self.icn_notification = IconFrame(
            self.frm_hBar, 'resources/icons/ui/bell_outline.png', 0, None, 32,
            lambda e: self.show_popup(
                self.to_window_coords(e.x_root, e.y_root)[0] - 360,
                self.to_window_coords(e.x_root, e.y_root)[1] + 20,
                # BOOKMARK_DONE: notification data list
                Container.filter(Notification,Notification.recipient == SessionWindow.ACTIVE_USER, Notification.id.notin_(Container.filter(SeenNotification.notificationId.distinct(), SeenNotification.notificationId == Notification.id, Notification.type == NotificationType.INVITED.value))).all(), 
                self.configure_notif_listitem
            )
        )
        self.icn_discussion = IconFrame(
            self.frm_hBar, 'resources/icons/ui/discussion_outline.png', 0, None, 32,
            lambda e: self.show_popup(
                self.to_window_coords(e.x_root, e.y_root)[0] - 360, 
                self.to_window_coords(e.x_root, e.y_root)[1] + 20, 
                # BOOKMARK_DONE: discussion data list
                Container.filter(Message,Message.sessionId == Collaboration.sessionId,or_(Collaboration.userId == SessionWindow.ACTIVE_USER.id, and_(Message.sessionId == Session.id, Session.ownerId == SessionWindow.ACTIVE_USER.id) ),Message.sentDate.in_(Container.filter(func.max(Message.sentDate)).group_by(Message.sessionId))).group_by(Message.sessionId).all(), 
                self.configure_msg_listitem
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