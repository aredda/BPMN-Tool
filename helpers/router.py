from views.windows.homewindow import HomeWindow
from views.windows.projectwindow import ProjectWindow
from views.windows.collaborationwindow import CollaborationWindow
from views.windows.discussionwindow import DiscussionWindow
from views.windows.editorwindow import EditorWindow
from views.windows.profilewindow import ProfileWindow
from views.windows.modals.messagemodal import MessageModal

def get_cls(route):
    
    if route == 'home': return HomeWindow
    if route == 'project': return ProjectWindow
    if route == 'collaboration': return CollaborationWindow
    if route == 'discussion': return DiscussionWindow
    if route == 'editor': return EditorWindow
    if route == 'profile': return ProfileWindow
    if route == 'messagemodal': return MessageModal

    return None


