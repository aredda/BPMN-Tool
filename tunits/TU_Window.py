from views.windows.abstract.window import Window
from views.windows.abstract.sessionwindow import SessionWindow
from views.windows.abstract.tabbedwindow import TabbedWindow
from views.windows.homewindow import HomeWindow
from views.windows.projectwindow import ProjectWindow
from views.windows.collaborationwindow import CollaborationWindow
from views.windows.profilewindow import ProfileWindow
from views.windows.discussionwindow import DiscussionWindow
from views.windows.editorwindow import EditorWindow
from views.components.scrollableframe import Scrollable
from tkinter import *
from resources.colors import *

def run():
    # window = HomeWindow()
    # window = ProjectWindow()
    # window = CollaborationWindow()
    # window = ProfileWindow()
    # window = DiscussionWindow()
    window = EditorWindow()

    window.mainloop()
