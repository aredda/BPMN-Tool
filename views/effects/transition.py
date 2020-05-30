import time
import threading

class Transition:
    
    def __init__(self, runnable):
        self.exit_time = False
        self.runnable = runnable

    def animate(self):
        threading.Thread(target=self.runnable).start ()

    def stop(self):
        self.exit_time = True