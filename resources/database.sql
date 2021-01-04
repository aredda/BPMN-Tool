CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    firstName VARCHAR(30),
    lastName VARCHAR(30),
    userName VARCHAR(40),
    email VARCHAR(100),
    `password` VARCHAR(50),
    `image` MEDIUMBLOB,
    company VARCHAR(30),
    gender ENUM('female', 'male')
);

CREATE TABLE relations(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    userOneId INTEGER NOT NULL,
    userTwoId INTEGER NOT NULL,
    FOREIGN KEY(userOneId) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(userTwoId) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE projects(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(50),
    file MEDIUMBLOB,
    creationDate DATETIME,
    lastEdited DATETIME,
    image MEDIUMBLOB,
    ownerId INTEGER NOT NULL,
    FOREIGN KEY(ownerId) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE sessions(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(50),
    creationDate DATETIME,
    ownerId INTEGER NOT NULL,
    projectId INTEGER NOT NULL,
    FOREIGN KEY(ownerId) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(projectId) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE collaborations(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    joiningDate DATETIME,
    privilege ENUM('read', 'edit'),
    userId INTEGER NOT NULL,
    sessionId INTEGER NOT NULL,
    FOREIGN KEY(userId) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(sessionId) REFERENCES sessions(id) ON DELETE CASCADE
);

CREATE TABLE history(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    editDate DATETIME,
    file MEDIUMBLOB,
    image MEDIUMBLOB,
    editorId INTEGER NOT NULL,
    projectId INTEGER NOT NULL,
    FOREIGN KEY(editorId) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(projectId) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE messages(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    content TEXT,
    sentDate DATETIME,
    userId INTEGER NOT NULL,
    sessionId INTEGER NOT NULL,
    FOREIGN KEY(userId) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(sessionId) REFERENCES sessions(id) ON DELETE CASCADE
);

CREATE TABLE notifications(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    `type` ENUM('recievedInv', 'acceptedInv','declinedInv','joinedViaLink'),
    notificationTime DATETIME,
    nature ENUM('invitation','invitationLink','shareLink'),
    invitationId INTEGER NOT NULL,
    actorId INTEGER NOT NULL,
    recipientId INTEGER NOT NULL,
    FOREIGN KEY(actorId) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(recipientId) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE invitations(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    privilege ENUM('read', 'edit'),
    invitationTime DATETIME,
    `status` ENUM('pending','accepted','rejected') NOT NULL DEFAULT 'pending',
    senderId INTEGER NOT NULL,
    recipientId INTEGER NOT NULL,
    sessionId INTEGER NOT NULL,
    FOREIGN KEY(senderId) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(recipientId) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(sessionId) REFERENCES sessions(id) ON DELETE CASCADE
);

CREATE TABLE invitationLinks(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    link TEXT,
    expirationDate DATETIME,
    privilege ENUM('read', 'edit'),
    senderId INTEGER NOT NULL,
    sessionId INTEGER NOT NULL,
    FOREIGN KEY(senderId) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(sessionId) REFERENCES sessions(id) ON DELETE CASCADE
);

CREATE TABLE shareLinks(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    link TEXT,
    expirationDate DATETIME,
    privilege ENUM('read', 'edit'),
    projectId INTEGER NOT NULL,
    FOREIGN KEY(projectId) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE sparePwd(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    expirationDate DATETIME,
    verificationCode TEXT,
    userId INTEGER NOT NULL,
    FOREIGN KEY(userId) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE seenNotifications(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    `date` DATETIME,
    seerId INTEGER NOT NULL,
    notificationId INTEGER NOT NULL,
    FOREIGN KEY(seerId) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(notificationId) REFERENCES notifications(id) ON DELETE CASCADE
);

CREATE TABLE seenMessages(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    `date` DATETIME,
    seerId INTEGER NOT NULL,
    messageId INTEGER NOT NULL,
    FOREIGN KEY(seerId) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(messageId) REFERENCES messages(id) ON DELETE CASCADE
);
