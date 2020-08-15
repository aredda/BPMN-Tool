from helpers.router import *
from tkinter import Tk

class WindowManager:

    INSTANCE = None

    def __init__(self):

        if WindowManager.INSTANCE != None:
            raise Exception('There must be one and only Window Manager!')

        self.windows = []

        self.root = Tk()
        self.root.withdraw()

    def run(self, window):
        # Hide running window
        if self.running() != None:
            self.running().hide()
        # Configure close
        window.protocol ('WM_DELETE_WINDOW', lambda: self.close())
        # Pass window manager
        window.set_manager(self)
        # Initialize the window
        window.initialize()
        # Add the newly created window to the queue
        self.windows.append(window)
        # Focus on the new window
        window.show()
        # Center window
        window.center()
        # Refresh the new window
        window.refresh()
    
    def run_tag(self, route, *args, **keyargs):
        self.run((get_cls(route))(self.root, *args, **keyargs))

    def close(self):
        # Retrieve opened
        running = self.windows.pop()
        # Configure on destroy
        running.destroy()
        # If there's no window in the background, then close application
        if self.running() == None:
            self.root.destroy()
        else:
            if self.running().__class__.__name__ in ['DiscussionWindow','HomeWindow']: 
                window = self.running().__class__(self.running().master)
                if self.running().__class__.__name__ == 'DiscussionWindow': 
                    for item in window.msgItems:
                        if item.dataObject.session == self.running().currentItem.dataObject.session:
                            window.Configure_session(None, item)
                self.windows.pop(len(self.windows)-1)
                window.set_manager(self)
                self.windows.append(window)
            #     self.run(window)
            # else:
            self.running().show()
            self.running().refresh()

    def running(self):
        return None if len(self.windows) == 0 else self.windows[-1]

    def quit(self):
        self.root.destroy()

    # helper method
    def get_module(self, name: str):
        return get_cls(name)
