from tkinter import *
from views.windows.abstract.window import Window
from views.windows.abstract.sessionwindow import SessionWindow
from views.components.tabmanager import TabManager
from views.components.tabhead import TabHead
from resources.colors import *

class TabbedWindow(SessionWindow):

    def __init__(self, tabSettings: list, title='Tabbed Window', width=Window.DEFAULT_WIDTH, height=Window.DEFAULT_HEIGHT, **args):
        SessionWindow.__init__(self, title, width, height, **args)

        self.tabSettings = tabSettings

        self.tbm_manager = TabManager(self.frm_body, bg=background)
        self.tb_container = Frame(self.frm_body, bg=background)

        self.tbm_manager.pack(side=TOP, fill=X)
        self.tb_container.pack(side=TOP, fill=BOTH, expand=1)

        # Set up tab heads
        self.config_tabHeads()

    def config_tabHeads(self):
        # Empty tab manager
        for child in self.tbm_manager.winfo_children():
            child.destroy()
        # Instantiate tab heads
        for i in self.tabSettings:
            self.tbm_manager.add_head(i.get('tag', 'tb_' + str(self.tabSettings.index(i))), TabHead(self.tbm_manager, i.get('text', 'Tab Head'), f'resources/icons/ui/{i["icon"]}', bg=background))

    
