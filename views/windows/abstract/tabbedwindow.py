from tkinter import *
from views.windows.abstract.window import Window
from views.windows.abstract.sessionwindow import SessionWindow
from views.components.tabmanager import TabManager
from views.components.tabhead import TabHead
from resources.colors import *

class TabbedWindow(SessionWindow):

    def __init__(self, root, tabSettings: list, title='Tabbed Window', width=Window.DEFAULT_WIDTH, height=Window.DEFAULT_HEIGHT, **args):
        SessionWindow.__init__(self, root, title, width, height, **args)

        self.tabSettings = tabSettings

        self.tbm_manager = TabManager(self.frm_body, bg=background)
        self.tb_container = Frame(self.frm_body, bg=background)

        self.tbm_manager.pack(side=TOP, fill=X)
        self.tb_container.pack(side=TOP, fill=BOTH, expand=1, pady=(15, 0))

        # Set up tab heads
        self.config_tabHeads()

    def config_tabHeads(self):
        # Empty tab manager
        for child in self.tbm_manager.winfo_children():
            child.destroy()
        # Instantiate tab heads and their corresponding body
        for i in self.tabSettings:
            self.tbm_manager.add_head(i.get('tag', 'tb_' + str(self.tabSettings.index(i))), TabHead(self.tbm_manager, i.get('text', 'Tab Head'), f'resources/icons/ui/{i["icon"]}', bg=background))
            # Create the body for this head
            tb_body = Frame(self.tb_container, bg=background)
            # Create an attr for this body
            setattr(self, i.get('tag'), tb_body)
            # Connect body
            self.connect_body_to(i.get('tag'), tb_body)
        # Finish tabbing
        self.finish_tabbing()

    def connect_body_to(self, tag, body):
        self.tbm_manager.connect_body(tag, body)

    def finish_tabbing(self):
        self.tbm_manager.initialize()
    
