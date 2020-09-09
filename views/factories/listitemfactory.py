from tkinter import *
from resources.colors import *
from views.factories.factory import Factory
from views.components.listitem import ListItem
from views.components.icon import IconFrame 
from models.entities.enums.notificationtype import NotificationType
from views.factories.iconbuttonfactory import *
import datetime

from helpers.backhelper import getNotificationContent
from helpers.imageutility import getdisplayableimage
from models.entities.enums.notificationtype import NotificationType
from models.entities.enums.notificationnature import NotificationNature 
from models.entities.enums.status import Status
from models.entities.Container import Container
from models.entities.Entities import Invitation, Notification, SeenNotification, Collaboration, Relation
import datetime


class ListItemFactory(Factory):

    def get_instance(listItemName: str):
        Factory.CLASS = ListItemFactory
        return Factory.get_instance()

    # Notification list item
    # BOOKMARK:  find a way to get the Container data
    def NotificationListItem(root, dataItem):
        # creation method of notification list item
        def create(item: ListItem):
            # we have three horizontal sections
            image = item.bindings.get('image')
            img_icon = IconFrame(item, image if image!= None else 'resources/icons/ui/face.png', 2, teal, 48)
            img_icon.pack(side=LEFT, anchor=N+W)

            frm_body = Frame(item, bg=white)
            frm_body.pack(side=LEFT, fill=BOTH, expand=1, padx=(10, 0))

            item.lbl_content = Label(frm_body, wraplength=200, fg=black, bg=white, font='-size 10 -weight bold', text=item.bindings.get('content', '{content}'), pady=0, padx=0)
            item.lbl_content.pack(side=TOP, anchor=N+W, pady=(0, 10))

            if item.buttonSettings != None:
                item.frm_btn_container = Frame(frm_body, bg=white)
                item.frm_btn_container.pack(side=TOP, expand=1, fill=BOTH)

                for s in item.buttonSettings:
                    btn = IconButton(
                        item.frm_btn_container, 
                        s.get('text', 'Button Text'), 
                        '-size 9 -weight bold', 
                        (teal if s.get('mode', 'main') == 'main' else white), 
                        'resources/icons/ui/' + s.get('icon', 'error.png'),
                        2, None,
                        (teal if s.get('mode', 'main') == 'main' else danger),
                        24,
                        s.get('cmnd', None),
                        bg=(white if s.get('mode', 'main') == 'main' else danger), padx=5, pady=5
                    )
                    if s.get('mode', 'main') == 'main':
                        btn.config(highlightthickness=1, highlightbackground=border)
                    btn.pack(side=LEFT, padx=(0, 5))

            lbl_label = Label(item, text=item.bindings.get('time', '{time}'), fg=gray, bg=white, font='-size 8')
            lbl_label.pack(side=RIGHT, anchor=N)
            # configure item
            item.config(bg=white, padx=8, pady=10)
        # BOOKMARK_DONE: notification list item, bindings should be configured here
        li= ListItem(root, dataItem, {
            'content': getNotificationContent(dataItem),
            'time': dataItem.notificationTime.strftime("%d/%m/%Y") if datetime.datetime.now().strftime("%x") != dataItem.notificationTime.strftime("%x") else dataItem.notificationTime.strftime("%X")  ,
            'image': dataItem.actor.image
        },
        # BOOKMARK_DONE: notification list item buttons 
        # (check if notification is invite , if not send None as a param and add command when the user accept/decline cmnd)
        [
            {
                'text': 'Accept',
                'icon': 'yes.png',
                'cmnd': lambda e: ListItemFactory.decision(li)
            },
            {
                'text': 'Decline',
                'icon': 'no.png',
                'mode': 'danger',
                'cmnd': lambda e: ListItemFactory.decision(li, accepted= False)
            }
        ] if dataItem.type == NotificationType.INVITED.value else None , create, bg=white)

        return li
    
    def decision(li, accepted= True):
        try:
            inv = Container.filter(Invitation).get(li.dataObject.invitationId)
            date = datetime.datetime.now()
            noti = None
            # if invitation is accepted
            if accepted:
                # create relations if they don't exist
                if Container.filter(Relation,Relation.userOne == inv.recipient, Relation.userTwo == inv.sender ).first() == None: Container.save(Relation(userOne= inv.recipient, userTwo= inv.sender))
                if Container.filter(Relation,Relation.userTwo == inv.recipient, Relation.userOne == inv.sender ).first() == None: Container.save(Relation(userTwo= inv.recipient, userOne= inv.sender))
                # create collaboration
                Container.save(Collaboration(joiningDate= date, privilege= inv.privilege, user= inv.recipient, session= inv.session))
                # add an acceptedInv type notification
                noti = Notification(notificationTime= date, type= NotificationType.ACCEPTED.value, nature= NotificationNature.INV.value, invitationId= inv.id, actor= inv.recipient, recipient= inv.sender)
                inv.status = Status.ACCEPTED.value
                if callable(getattr(li.window, "refresh_window", None)):
                    li.window.refresh_window()
            # if invitation is accepted
            else:
                # add a rejectedInv type notification
                noti = Notification(notificationTime= date, type= NotificationType.DECLINED.value, nature= NotificationNature.INV.value, invitationId= inv.id, actor= inv.recipient, recipient= inv.sender)
                inv.status = Status.REJECTED.value
        except: pass
        finally:
            # save the recieved invitation as recieved
            seenNoti = SeenNotification(date= date, seer= inv.recipient, notification= li.dataObject)
            Container.save(seenNoti, noti, inv)

        # if it's a recievedInv kind of Notifications
        if hasattr(li,'frm_btn_container'):
            # change the listItem message 
            li.lbl_content['text'] = f'you have joined ({inv.session.title})' if inv.status == Status.ACCEPTED.value else f'invitation to ({inv.session.title}) declined'
            #  hide the buttons
            li.frm_btn_container.pack_forget()

    def DiscussionListItem(root, dataItem):
        def create(item: ListItem):
            item.config(bg=white, pady=10, padx=10)
            item.pack(side=TOP, fill=X)

            image = item.bindings.get('image')
            item.img_photo = IconFrame(item, image if image!= None else 'resources/icons/ui/face.png', 2, teal, 40)
            item.img_photo.pack(side=LEFT)

            item.frm_content = Frame(item, bg=white, padx=5)
            item.frm_content.pack(side=LEFT)

            item.lbl_username = Label(item.frm_content, fg=teal, bg=white, text=item.bindings.get('session', '{session}'), font='-size 12 -weight bold')
            item.lbl_username.pack(side=TOP, anchor=N+W)
            
            item.lbl_user = Label(item.frm_content, fg=black, font='-size 10 -weight bold', bg=white, text=item.bindings.get('username', '{username}')+':')
            item.lbl_user.pack(side=LEFT, anchor=N+W)

            item.lbl_content = Label(item.frm_content, fg=black, bg=white, anchor=W, text=item.bindings.get('content', '{content}'))
            item.lbl_content.pack(side=LEFT, anchor=N+W)

            item.lbl_time = Label(item, bg=white, fg=gray, text=item.bindings.get('time', '{time}'), font='-size 8', pady=5)
            item.lbl_time.pack(side=RIGHT, anchor=N)

        # BOOKMARK_DONE: configure discussion list item
        return ListItem(root, dataItem, {
            'session': dataItem.session.title if len(dataItem.session.title) < 20 else (dataItem.session.title[17] + '...'),
            'username': dataItem.user.userName,
            'content': dataItem.content if len(dataItem.content) < 10 else (dataItem.content[:7] + '...'),
            'time': dataItem.sentDate.strftime("%d/%m/%Y") if datetime.datetime.now().strftime("%x") != dataItem.sentDate.strftime("%x") else dataItem.sentDate.strftime("%X"),
            'image': dataItem.user.image
        }, None, create)

    def GuideItem(root, dataDict, descriptionWidth):
        # specify creation method
        def create(item):
            # term
            item.lbl_term = Label(item, anchor=W, width=15, font='-size 14 -weight bold', text=dataDict.get('term', '(term) not found'), fg=teal, bg=background)
            item.lbl_term.pack(side=LEFT, fill=X, expand=1, pady=7)
            # description
            item.lbl_description = Label(item, anchor=W, font='-size 12 -weight bold', text=dataDict.get('description', '(description) not found'), fg=gray, bg=background, wraplength=descriptionWidth, width=descriptionWidth)
            item.lbl_description.pack(side=RIGHT, fill=X, expand=1, pady=7)
            # item settings
            item.config(bg=background)
        # return item
        return ListItem(root, None, None, None, create)

