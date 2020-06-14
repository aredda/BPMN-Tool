from tkinter import *
from views.windows.abstract.modal import Modal
from views.components.icon import IconFrame
from resources.colors import *

class MessageModal(Modal):

    # Modal types
    INFO = 'info'
    ERROR = 'error'
    PROMPT = 'prompt'

    def __init__(self, root, title: str, message: str, messageType: str = 'error', actions: dict = None, **args):
        
        # Prepare modal buttons
        buttons = [
            {
                'text': 'Okay',
                'icon': 'yes.png',
                'cmnd': lambda e: self.destroy()
            }
        ]

        if actions != None:
            buttons = [
                {
                    'text': 'No',
                    'icon': 'no.png',
                    'cmnd': actions.get('no', lambda e: self.destroy()),
                    'mode': 'danger'
                },
                {
                    'text': 'Yes',
                    'icon': 'yes.png',
                    'cmnd': actions.get('yes', None)
                }
            ]
        
        Modal.__init__(self, root, title, buttons, self.MODAL_WIDTH, 325, **args)

        color = black if messageType == self.PROMPT else (teal if messageType == self.INFO else danger)

        img_icon = IconFrame(self.frm_body, 'resources/icons/ui/' + messageType + '.png', 6, color, 75)
        img_icon.pack(side=LEFT)
        
        lbl_message = Label(self.frm_body, text=message, bg=background, fg=color, font='-size 15 -weight bold', justify=LEFT, wraplength=self.MODAL_WIDTH-150)
        lbl_message.pack(side=LEFT, padx=(10, 0))