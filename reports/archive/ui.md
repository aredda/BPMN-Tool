# User Interfaces
All of the views plus all of their mechanisms.

### Splash Screen
The purpose behind this view is to make the user wait until the resources are fully ready,
and display some functionalities as a **Slider**, not to mention list the credits to the developers.

### Sign in Screen
This screen will contain a login form:
- **[Username | Email]** and **Password** fields
- **Remember Me** option
- **Forgotten password?** option

### Sign up Screen
This view will consist of 3 stages:
- Submitting **First Name**, **Last Name** and **Email**
- Submitting **Username**, **Password** and **Password's Confirmation**
- Submitting **Gender**, **Company** and **Image**

### Home Screen
This view contains:
-  a **Tab** of projects:
   -  Listing all projects in form of cards [Title | Creation Date | Last Edit Date | Image]
   -  Possibility to [**create** | **open** | **delete**] a project
   -  Possibility to [**export as SVG** | **export as XML**] a project
   -  Possibility to **import an XML file and create** a project
   -  Possibility to **share a project** by creating a share link
-  a **Tab** of collaboration sessions:
   - Listing all sessions in form of cards [Image | Session's Title | Creation Date | Last Edit | Number of collabortors]
   - Possibility to **create** a session
   - Possibility to **leave** a session
   - **[Administrator | Owner]** has the right to **remove/disband** the session

### Project Screen
Responsible for:
- a **Tab** that consists of *Project's information* [Title, Creation Date, Last Edit Date]
- a **Tab** that shows a list of history changes
  - With the possibility to revert to a specific edit
- Exporting options:
  - Exporting as XML
  - Exporting as SVG
- Open project in the *Editor Window*

### Session Screen
Takes care of:
- a **Tab** that shows the *Session and Project* information
  - The list of collaborators
  - **[Only for administrator]** remove a collaborator from the collaborators list
- a **Tab** for the history of changes
  - **[Only for administrator]** With the possibility to revert to a past version/edit
  - **[Only for administrator]** With the possibility to disband and delete the session
- Possibility to leave the session and end your collaboration
- Open Editor Window to edit project

### Discussion Screen
- a **Section** that shows all of started discussions between sessions
- a **Section** that shows the messages of **one discussion**
  - Possibility to open the **Session Window** of the selected discussion

### Editor Screen
- A **Panel** whose content is all the modeling elements
- A Work **Panel** where elements are placed and handled
- Exporting options:
  - Export as XML
  - Export as SVG

### Profile
- A **Tab** that contains a form of personal information
  - Change information
  - Delete account
- A **Tab** that contains a list of relations with collaborators
  - Remove a collaborator from the list

### Shared Fragments
All screens will share some components:
- A **Header**
  - A Notification indicator (icon) that displays a notification pop-up
  - A Message indicator (icon) that displays a discussion pop-up
  - An ImageButton that shows the image of the user and his username that redirects to the Profile Screen

### Other Components:
The experience will need:
- A Menu Drop-Down
- Transition effects
- A Loader
- A Slider