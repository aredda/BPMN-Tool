from tkinter import *
from views.windows.abstract.modal import Modal
from views.components.scrollable import Scrollable
from views.factories.listitemfactory import ListItemFactory
from views.factories.iconbuttonfactory import MainButton

class GuideModal(Modal):

    INSTRUCTIONS = [
        {
            'term': 'Escape',
            'description': 'Cancel an action'
        },
        {
            'term': 'Cntrl + Z',
            'description': 'Undo an action'
        },
        {
            'term': 'Cntrl + Y',
            'description': 'Redo an action'
        },
        {
            'term': 'Cntrl + V',
            'description': 'Reset canvas view'
        },
        {
            'term': 'Cntrl + S',
            'description': 'Save changes'
        },
        {
            'term': 'Cntrl + I',
            'description': 'Zoom In'
        },
        {
            'term': 'Cntrl + O',
            'description': 'Zoom Out'
        },
        {
            'term': 'Cntrl + L',
            'description': 'Enter SELECTION mode'
        },
        {
            'term': 'Cntrl + M',
            'description': 'Enter MOVE_CANVAS_VIEW mode'
        },
        {
            'term': 'Cntrl + H',
            'description': 'Show keyboard shortcuts'
        }
    ]

    def __init__(self, root):
        super().__init__(root, 'Editor Keyboard Shortcuts', None, self.MODAL_WIDTH, 510)

        self.frm_scrollable = Scrollable(self.frm_body)
        self.frm_scrollable.pack(fill=BOTH, expand=1)

        for inst in self.INSTRUCTIONS:
            ListItemFactory.GuideItem(self.frm_scrollable.interior, inst, self.DEFAULT_WIDTH - 100).pack(side=TOP, fill=X)

        self.btn_footer_close = MainButton(self.frm_footer, 'Close', 'cancel.png', lambda e: self.destroy())
        self.btn_footer_close.pack(side=RIGHT)
