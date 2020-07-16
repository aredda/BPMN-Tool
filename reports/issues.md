# General issues
- [X] The necessity of re-organizing the structure of 'models' folder; models should be categorized
because we are going to add other models concerning data..
- [X] The scrollable frame is no longer working
- [X] Implementing Anti-Alias For Drawn Elements
- [X] Window Manager (+ Fade Effect)
- [X] Change name conventions for the old model folder
- [ ] Adding an image to Profile Window's Form (To upload and show profile photo)
- [ ] Minor updates of database
  - Notification, should have a new field that indicates if the notification is read or not
  - A new table Seen, indicates if a message is seen or not
  - Invitation table should have a field that describes the decision of the recepient
  - Notification table should have a field that descriminates the nature of Invitation [InvitationLink | ShareLink | InvitationLink]

# Deserialization
- [X] SubProcess
- [X] Lanes
- [X] TextAnnotation and its associations
- [X] Message Flows
- [X] BPMNDI section
- [X] Activity Flag Serialization
- [X] Extra data object for no goddamn reason
- [X] BPMN edges don't find their elements
- [ ] ~~Group Serialization & Deserialization~~

# Modals
### Window
- [X] A message modal for dispaying **information**, **error** and **confirmation** messages
### SessionWindow
- [X] Notification, Discussion modals
### HomeWindow
- [X] Create a new project modal
- [X] Create a project from existing source modal
- [X] Create a new collaboration session
- [X] Joining a project/session using a link modal
### ProjectWindow
- [X] Share modal
### SessionWindow
- [X] Invite modal

# Minor Issues and things that should be optimised
### Session Window 
- [ ] Discussion image doesn't show
- [ ] notification image doesn't show
### Saved Collaborators
- [ ] collaborator's image doesn't show
- [ ] listItem width issue when the number is impair
### discussion window 
- [ ] scrollbar should be at the end when we enter a session + minor issue when switching between sessions / issue on discussions switch
- [ ] hide session's name section and textmessage part
### profile window
- [ ] password and confirmPwd must be hidden
- [ ] MessageModal button disappears when message is big
### form modal factory in home window
- [ ] modal interfers with openfiledialog 
### collaboration window
- [ ] members listItem issue (size and kick button)
- [ ] image resizing issue
### ListItem
- [ ] when content is long we can't see the rest of it and the date

- [ ] DEBUG WEIRD SQL/THREAD ERRORS 