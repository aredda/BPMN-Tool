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
            self.running().withdraw()
        # Configure close
        window.protocol ('WM_DELETE_WINDOW', lambda: self.close())
        # Pass window manager
        window.set_manager(self)
        # Add the newly created window to the queue
        self.windows.append(window)
        # Focus on the new window
        window.deiconify()
        # Refresh the new window
        window.refresh()
    
    def run_tag(self, route):
        self.run((get_cls(route))(self.root))

    def close(self):
        # Retrieve opened
        running = self.windows.pop()
        # Configure on destroy
        running.destroy()
        # If there's no window in the background, then close application
        if self.running() == None:
            self.root.destroy()
        else:
            self.running().deiconify()
            self.running().refresh()

    def running(self):
        return None if len(self.windows) == 0 else self.windows[-1]
