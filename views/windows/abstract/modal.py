from resources.colors import *
from tkinter import *
from views.windows.abstract.window import Window
from views.components.icon import IconFrame
from views.components.iconbuttonfactory import *

class Modal(Window):
    
    MODAL_WIDTH = 640
    MODAL_HEIGHT = 480

    def __init__(self, root, title, buttons: dict = None, **args):
        Window.__init__(self, root, title, Modal.MODAL_WIDTH, Modal.MODAL_HEIGHT, **args)

        # Header
        self.frm_header = Frame(self, bg=white, padx=20, pady=20)
        self.frm_header.pack(side=TOP, fill=X)
        self.lbl_title = Label(self.frm_header, text=title, bg=white, fg=black, font='-size 20 -weight bold')
        self.lbl_title.pack(side=LEFT)
        self.btn_close = IconFrame(self.frm_header, 'resources/icons/ui/cancel.png', 5, black, 50, lambda e: self.destroy(), danger)
        self.btn_close.pack(side=RIGHT)
        self.frm_header.update()

        # Header Bottom Border
        self.frm_border_bottom = Frame(self, highlightthickness=1, highlightbackground=border)
        self.frm_border_bottom.pack(side=TOP, fill=X)

        # Body
        self.frm_body = None

        # Footer
        self.frm_footer = Frame(self, bg=silver, padx=15, pady=15)
        self.frm_footer.pack(side=BOTTOM, fill=X)

        if buttons != None:
            for button in buttons:
                btn = (DangerButton if button.get('mode', 'main') == 'danger' else MainButton)(self.frm_footer, button.get('text', 'Text'), button.get('icon', 'error.png'), button.get('cmnd', None))
                btn.pack(side=RIGHT, padx=(10, 0))

        # Footer Bottom Border
        self.frm_border_top = Frame(self, highlightthickness=1, highlightbackground=border)
        self.frm_border_top.pack(side=BOTTOM, fill=X)

        self.grab_set_global()
        self.resizable(False, False)