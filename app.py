from tkinter import *
from helpers.windowmanager import WindowManager
from views.windows.abstract.modal import Modal
from views.windows.modals.messagemodal import MessageModal
from views.windows.modals.formmodal import FormModal
from views.windows.modals.formmodalfactory import *

# manager = WindowManager()
# manager.run_tag('home')
# manager.root.mainloop()

root = Tk()

LoadProjectModal(root, lambda modal: print (modal.get_form_data()))

root.mainloop()
