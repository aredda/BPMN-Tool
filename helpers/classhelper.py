from views.windows.homewindow import HomeWindow
from views.windows.projectwindow import ProjectWindow
from views.windows.collaborationwindow import CollaborationWindow
from views.windows.discussionwindow import DiscussionWindow
from views.windows.editorwindow import EditorWindow
from views.windows.profilewindow import ProfileWindow

def get_cls(tag):
    
    if tag == 'home': return HomeWindow
    if tag == 'project': return ProjectWindow
    if tag == 'collaboration': return CollaborationWindow
    if tag == 'discussion': return DiscussionWindow
    if tag == 'editor': return EditorWindow
    if tag == 'profile': return ProfileWindow

    return None


