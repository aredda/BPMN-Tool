from tkinter import *
from resources.colors import *
from views.windows.abstract.tabbedwindow import TabbedWindow
from views.components.listitem import ListItem
from views.components.icon import IconFrame
from views.components.iconbuttonfactory import *
from views.components.scrollable import Scrollable

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

    btnSettings = [
        {
            'icon': 'open.png',
            'text': 'Open Editor',
            'dock': LEFT
        },
        {
            'icon': 'delete.png',
            'text': 'End Session',
            'type': DangerButton
        },
        {
            'icon': 'invite.png',
            'text': 'Invite',
            'type': SecondaryButton
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

    def __init__(self, session=None, **args):
        TabbedWindow.__init__(self, CollaborationWindow.tabSettings, 'Session\'s Title', **args)

        # Design elements
        self.design()
        # Fill session members
        self.fill_members()

    def design(self):
        # Putting the control buttons
        btn_container = Frame(self.frm_body, bg=background)
        btn_container.pack(fill=X, side=TOP)

        for i in CollaborationWindow.btnSettings:
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
        frm_preview.pack(side=LEFT, fill=BOTH, expand=1)

        self.lv_members = Scrollable(frm_group, bg=background)
        self.lv_members.pack(side=RIGHT, fill=BOTH, padx=(10, 0))

        # Filling the history tab
        self.frm_list_view = Scrollable(self.tb_hist, bg=background)
        self.frm_list_view.pack(expand=1, fill=BOTH, pady=(0, 15))

        # BOOKMARK: Fill Collaboration Session Change History
        for i in range(10):
            ListItem(self.frm_list_view.interior, None, None, [
                {
                    'icon': 'save.png',
                    'text': 'Export to XML'
                },
                {
                    'icon': 'revert_history.png',
                    'text': 'Revert'
                }
            ]).pack(anchor=N+W, fill=X, pady=(0, 10), padx=5)

    # BOOKMARK: Fill Collaboration Session Members
    def fill_members(self):
        # Remove all items
        self.lv_members.empty()
        # Append items
        for i in range(6):
            ListItem(self.lv_members.interior, None, None, [
                {
                    'icon': 'cancel.png',
                    'text': 'Kick'
                }
            ]).pack(anchor=N+W, pady=(0, 10), padx=(0, 10))