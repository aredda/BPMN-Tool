from tkinter import *
from resources.colors import *
from views.windows.abstract.tabbedwindow import TabbedWindow
from views.components.listitem import ListItem
from views.components.icon import IconFrame
from views.components.iconbuttonfactory import *
from views.components.scrollable import Scrollable

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

    btnSettings = [
        {
            'icon': 'open.png',
            'text': 'Open Editor',
            'dock': LEFT
        },
        {
            'icon': 'share.png',
            'text': 'Share Project',
            'type': SecondaryButton
        },
        {
            'icon': 'save.png',
            'text': 'Export as SVG'
        },
        {
            'icon': 'save.png',
            'text': 'Export as XML'
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

    def __init__(self, project=None, **args):
        TabbedWindow.__init__(self, ProjectWindow.tabSettings, 'Project\'s Title', **args)

        # Design elements
        self.design()

    def design(self):
        # Putting the control buttons
        btn_container = Frame(self.frm_body, bg=background)
        btn_container.pack(fill=X, side=TOP)

        for i in ProjectWindow.btnSettings:
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

        # Filling the history tab
        self.frm_list_view = Scrollable(self.tb_hist, 0, bg=background)
        self.frm_list_view.pack(expand=1, fill=BOTH, pady=(0, 15))

        for i in range(5):
            self.frm_list_view.pack_item(ListItem(self.frm_list_view, None, None, [
                {
                    'icon': 'save.png',
                    'text': 'Export to XML'
                },
                {
                    'icon': 'revert_history.png',
                    'text': 'Revert'
                }
            ]), fill=X)