from tkinter import *
from tkinter.filedialog import *
from resources.colors import *
from views.factories.iconbuttonfactory import SecondaryButton, MainButton
from views.windows.modals.formmodal import FormModal

# BOOKMARK: how to create a command for form modal buttons
# the concept behind those buttons is that we need to be in contact with the modal object itself
# because it contains our form data and our connection to the database and everything else..
# in order to solve this, I propose to construct a command in this form
#
#   def command(modal): # do something
# or
#   lambda modal: # do something
#
# this way, we can access our modal from outside, and the object doesn't even have to be created in the first place

class FormModalFactory:

    #####
    ### factory method
    #####
    def get_modal(modalName: str):
        # retrieve the list of static methods
        staticmethods = [method for method in dir(FormModalFactory) if 'Modal' in method]
        # retrieve the targeted modal
        if modalName in staticmethods: return getattr(FormModalFactory, modalName)
        # otherwise return None
        return None

    # Invitation Modal
    def InviteModal(root, linkCommand, inviteCommand):
        inputs = [
            {
                'label': 'Generated Invitation Link:',
                'icon': 'link.png',
                'name': 'txt_link'
            },
            {
                'label': 'Invite Collaborator by his username:',
                'icon': 'account.png',
                'name': 'txt_username'
            }
        ]
        buttons = [
            {
                'text': 'Activate Link',
                'icon': 'link.png',
                'cmnd': linkCommand
            },
            {
                'text': 'Invite Collaborator',
                'icon': 'invite.png',
                'cmnd': inviteCommand
            }
        ]
        return FormModal(root, 'Invite Collaborators', 450, inputs, buttons)

    # Sharing Modal
    def ShareModal(root, linkCommand):
        inputs = [
            {
                'label': 'Generated Share Link:',
                'icon': 'link.png',
                'name': 'txt_link'
            }
        ]
        buttons = [
            {
                'text': 'Activate Link',
                'icon': 'link.png',
                'cmnd': linkCommand
            }
        ]
        return FormModal(root, 'Share Project Via Link', 340, inputs, buttons)

    # Joining Modal
    def JoinModal(root, joinCommand):
        inputs = [
            {
                'label': 'Project/Session Link:',
                'icon': 'link.png',
                'name': 'txt_link'
            }
        ]
        buttons = [
            {
                'text': 'Join',
                'icon': 'login.png',
                'cmnd': joinCommand
            }
        ]
        return FormModal(root, 'Join a Session or access a Project', 340, inputs, buttons)

    # Creating a project Modal
    def CreateProjectModal(root, createCommand):
        inputs = [
            {
                'label': 'Project\'s Title:',
                'icon': 'folder.png',
                'name': 'txt_title'
            }
        ]
        buttons = [
            {
                'text': 'Create Project',
                'icon': 'new_project.png',
                'cmnd': createCommand
            }
        ]
        return FormModal(root, 'Create a new Project', 340, inputs, buttons)

    # Creating a session Modal
    def CreateSessionModal(root, createCommand):
        inputs = [
            {
                'label': 'Session\'s Title:',
                'icon': 'session.png',
                'name': 'txt_title'
            }
        ]
        buttons = [
            {
                'text': 'Create Session',
                'icon': 'new_session.png',
                'cmnd': createCommand
            }
        ]
        return FormModal(root, 'Create a new Session', 340, inputs, buttons)

    # Creating a project from opening 
    def LoadProjectModal(root, createCommand):
        inputs = [
            {
                'label': 'Project\'s Title:',
                'icon': 'folder.png',
                'name': 'txt_title'
            }
        ]
        buttons = [
            {
                'text': 'Create Project',
                'icon': 'new_project.png',
                'cmnd': createCommand
            }
        ]

        def onCreated(modal: FormModal):
            frm_group = Frame(modal.frm_body, bg=background)
            frm_group.pack(side=TOP, fill=X)
            
            # pick button event
            def btn_pick_click(e):
                # BOOKMARK: pick button click event
                # ask to open a certain xml file
                filepath = 'ask for file'
                # verify if file exists
                # change the value of label
                modal.lbl_filename['text'] = filepath

            # pick file button
            btn_pick = MainButton(frm_group, 'Pick a file', 'upload.png', btn_pick_click)
            btn_pick.pack(side=LEFT)

            # file path label
            modal.lbl_filename = Label(frm_group, text='Pick an XML file...', bg=background, fg=gray, font='-size 10', anchor=N+W)
            modal.lbl_filename.pack(side=RIGHT, fill=X, expand=1, padx=(5, 0))

            # register label as a form input
            modal.form.append({
                'name': 'txt_filepath',
                'input': modal.lbl_filename,
                'getter': lambda input: input['text'] 
            })

        return FormModal(root, 'Create a new Project', 410, inputs, buttons, onCreated)