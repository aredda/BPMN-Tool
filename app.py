from tkinter import *
from helpers.windowmanager import WindowManager
from views.windows.abstract.modal import Modal
from views.windows.modals.messagemodal import MessageModal

manager = WindowManager()
manager.run_tag('home')
manager.root.mainloop()