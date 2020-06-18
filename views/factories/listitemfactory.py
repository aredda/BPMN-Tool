from tkinter import *
from resources.colors import *
from views.factories.factory import Factory
from views.components.listitem import ListItem
from views.components.icon import IconFrame 
from models.entities.enums.notificationtype import NotificationType
from views.factories.iconbuttonfactory import *
import datetime

class ListItemFactory(Factory):

    def get_instance(listItemName: str):
        Factory.CLASS = ListItemFactory
        return Factory.get_instance()

    # Notification list item
    def NotificationListItem(root, dataItem):
        # creation method of notification list item
        def create(item: ListItem):
            # we have three horizontal sections
            img_icon = IconFrame(item, 'resources/icons/ui/account.png', 2, teal, 48)
            img_icon.pack(side=LEFT, anchor=N+W)

            frm_body = Frame(item, bg=white)
            frm_body.pack(side=LEFT, fill=BOTH, expand=1, padx=(10, 0))

            lbl_content = Label(frm_body, fg=black, bg=white, font='-size 10 -weight bold', text=item.bindings.get('content', '{content}'), pady=0, padx=0)
            lbl_content.pack(side=TOP, anchor=N+W, pady=(0, 10))

            if item.buttonSettings != None:
                frm_btn_container = Frame(frm_body, bg=white)
                frm_btn_container.pack(side=TOP, expand=1, fill=BOTH)

                for s in item.buttonSettings:
                    btn = IconButton(
                        frm_btn_container, 
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
        # BOOKMARK: notification list item, bindings should be configured here
        return ListItem(root, dataItem, {
            'content': '{content}',
            'time': '{time}',
            'image': '{image}'
        }, 
        # BOOKMARK: notification list item buttons
        [
            {
                'text': 'Accept',
                'icon': 'yes.png'
            },
            {
                'text': 'Decline',
                'icon': 'no.png',
                'mode': 'danger'
            }
        ], create, bg=white)
    
    def DiscussionListItem(root, dataItem):
        def create(item: ListItem):
            item.config(bg=white, pady=10, padx=10)
            item.pack(side=TOP, fill=X)

            item.img_photo = IconFrame(item, 'resources/icons/ui/face.png', 10, teal, 40)
            item.img_photo.pack(side=LEFT)

            item.frm_content = Frame(item, bg=white, padx=5)
            item.frm_content.pack(side=LEFT)

            item.lbl_username = Label(item.frm_content, fg=teal, bg=white, text=item.bindings.get('session', '{session}'), font='-size 12 -weight bold')
            item.lbl_username.pack(side=TOP, anchor=N+W)
            
            item.lbl_content = Label(item.frm_content, fg=black, bg=white, text=item.bindings.get('content', '{content}'))
            item.lbl_content.pack(side=TOP, anchor=N+W)

            item.lbl_time = Label(item, bg=white, fg=gray, text=item.bindings.get('time', '{time}'), font='-size 8', pady=5)
            item.lbl_time.pack(side=RIGHT, anchor=N)

        # BOOKMARK: configure discussion list item
        return ListItem(root, dataItem, {
            'session': '{session}',
            'content': '{content}',
            'time': '{time}'
        }, None, create)