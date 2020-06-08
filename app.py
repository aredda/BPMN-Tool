from tkinter import *
from helpers.windowmanager import WindowManager
from views.windows.abstract.modal import Modal

# manager = WindowManager()
# manager.run_tag('editor')
# manager.root.mainloop()

root = Tk()

m = Modal(root, 'Okay Cokey', [
    {
        'text': 'Cancel',
        'icon': 'no.png',
        'mode': 'danger',
        'cmnd': lambda e: m.destroy()
    },
    {
        'text': 'Okay',
        'icon': 'yes.png'
    }
])
m.mainloop()