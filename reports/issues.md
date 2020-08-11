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
- [x] Discussion image doesn't show
- [x] notification image doesn't show
- [ ] Hide pop-ups when the mouse leaves them
### message listItem
- [x] long messages errors
### Saved Collaborators
- [ ] (mohamed) collaborator's image doesn't show **changing it affects profile image**
<!-- - [ ] listItem width issue when the number is impair **not a big deal** -->
### discussion window 
- [ ] (ibrahim) scrollbar should be at the end when we enter a session 
- [ ] (ibrahim) issue with the scrollbar when switching between sessions
- [ ] (ibrahim) hint can be sent when it shouldn't 
- [ ] Click on the whole item to open conversation
<!-- - [ ] hide session's name section and textmessage part **not a big deal** -->
### profile window
- [x] password and confirmPwd must be hidden
- [x] (mohamed) MessageModal button disappears when message is big
### form modal factory in home window
- [x] modal interfers with openfiledialog 
### collaboration window
- [ ] (ibrahim) members listItem issue (size and kick button)
- [ ] image width resizing issue, the image won't extend its original width **same issue**
### notification ListItem
- [ ] (ibrahim) when content is long we can't see the rest of it and the date
### home window
- [x] project and session image doesn't show
- ~~[ ] menu icon background transparency issue~~
### project window
- [ ] image width resizing issue the app won't extend its original width **same issue**
- [x] DEBUG WEIRD SQL/THREAD ERRORS **needs more tests**