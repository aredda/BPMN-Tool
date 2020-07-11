from tkinter import *
from resources.colors import *
from views.windows.abstract.sessionwindow import SessionWindow
from views.components.scrollable import Scrollable
from views.components.listitem import ListItem
from views.components.icon import IconFrame
from views.factories.iconbuttonfactory import *
from views.factories.listitemfactory import ListItemFactory

from models.entities.Entities import Collaboration,Session,Message,SeenMessage
from models.entities.Container import Container
from sqlalchemy import and_,or_,func
import datetime
from views.windows.collaborationwindow import CollaborationWindow

import time
import threading

class DiscussionWindow(SessionWindow):

    # Chat Session Item Styles
    CHAT_NORMAL = {
        'bg': white,
        'lbl_username': teal,
        'lbl_content': black,
        'lbl_time': gray 
    }
    CHAT_UNREAD = {
        'bg': background,
        'lbl_username': teal,
        'lbl_content': black,
        'lbl_time': gray 
    }
    CHAT_ACTIVE = {
        'bg': teal,
        'lbl_username': background,
        'lbl_content': white,
        'lbl_time': white 
    }

    # Message Item Styles
    MSG_INCOMING = CHAT_NORMAL
    MSG_OUTGOING = CHAT_ACTIVE

    def __init__(self, root, **args):
        SessionWindow.__init__(self, root, 'Discussions')
        
        self.currentItem = None

        self.design()

        self.msgItems = []

        self.fill_sessions()
        self.configure_session_click()

    def design(self):
        # Session items section
        self.frm_body.config(padx=0, pady=0)

        frm_sessions = Frame(self.frm_body, bg=background, width=250)
        frm_border = Frame(self.frm_body, highlightthickness=1, highlightbackground=border) 
        frm_discussion = Frame(self.frm_body, bg=background)

        frm_sessions.pack_propagate(0)

        self.lv_sessions = Scrollable(frm_sessions, bg=silver)
        self.lv_sessions.pack(fill=BOTH, expand=1)

        frm_sessions.pack(side=LEFT, fill=Y)
        frm_border.pack(side=LEFT, fill=Y)
        frm_discussion.pack(side=LEFT, fill=BOTH, expand=1)
        
        # Discussion Section
        frm_head = Frame(frm_discussion, bg=white, pady=20, padx=20)
        frm_head.pack(side=TOP, fill=X)

        frm_border_bottom = Frame(frm_discussion, highlightthickness=1, highlightbackground=border)
        frm_border_bottom.pack(fill=X, side=TOP)

        frm_group = Frame(frm_head, bg=white)
        frm_group.pack(side=LEFT, fill=X)

        self.lbl_sessionName = Label(frm_group, bg=white, fg=teal, text='Session\'s Name', font='-size 18 -weight bold')
        self.lbl_sessionName.pack(anchor=N+W)

        self.lbl_memberCount = Label (frm_group, bg=white, fg=black, text='X members')
        self.lbl_memberCount.pack(anchor=N+W)

        self.btn_open_session = MainButton(frm_head, 'Open Session', 'open.png',btnCmd=lambda event:self.open_session(event))
        self.btn_open_session.config(pady=5)
        self.btn_open_session.pack(side=RIGHT)

        frm_scrollable_container = Frame(frm_discussion, bg=black)
        frm_scrollable_container.pack_propagate(0)
        frm_scrollable_container.pack(side=TOP, fill=BOTH, expand=1)

        self.lv_messages = Scrollable(frm_scrollable_container, bg=background, padx=15, pady=15)
        self.lv_messages.pack(expand=1, fill=BOTH)

        frm_footer = Frame(frm_discussion, bg=white, pady=20, padx=20)
        frm_footer.pack(side=BOTTOM, fill=X)

        self.txt_message = Entry(frm_footer, highlightthickness=0, relief=FLAT, font='-size 12', fg=black)
        self.txt_message.insert(0, 'Type your message here...')
        self.txt_message.bind('<FocusIn>', lambda e: self.txt_message.delete(0, len(self.txt_message.get())))
        self.txt_message.pack(side=LEFT, fill=BOTH, expand=1)

        IconFrame(frm_footer, 'resources/icons/ui/send.png', 25, teal,command=lambda event: self.send_message(event,self.currentItem)).pack(side=RIGHT)

        frm_border_top = Frame(frm_discussion, highlightthickness=1, highlightbackground=border)
        frm_border_top.pack(side=BOTTOM, fill=X)

    def runnable(self):
        while self.time_to_kill != True:
            time.sleep(2)
            Container.session.commit()
            for li in self.msgItems:
                lastmsg = Container.filter(Message, Message.sessionId == li.dataObject.session.id).order_by(Message.sentDate.desc()).first()
                if lastmsg != None and lastmsg != li.dataObject:
                    li.lbl_content['text']=lastmsg.content
                    li.lbl_time['text'] = lastmsg.sentDate.strftime("%X")
                    li.dataObject = lastmsg
                    if self.currentItem != None and self.currentItem == li: 
                        self.currentItem = li
                        # self.fill_discussion(self.currentItem.dataObject.session)
                        self.create_message(lastmsg)

        
    def hide(self):
        # thread killer logic will be here
        self.time_to_kill = True
        print ('the thread shall stop now')
        # continute the original work
        super().hide()

    def refresh(self): 
        self.time_to_kill = False
        # start thread
        threading.Thread(target=self.runnable).start()

    def open_session(self, event):
        if self.currentItem != None:
            self.windowManager.run(CollaborationWindow(self,self.currentItem.dataObject.session))

    # Configure sessionlistitem click event
    def configure_session_click(self):
        def Configure_session(event, listItem):
            self.fill_discussion(listItem.dataObject.session)

            self.lbl_sessionName['text'] = listItem.dataObject.session.title
            self.lbl_memberCount['text'] = f'{Container.filter(Collaboration,Collaboration.sessionId == listItem.dataObject.session.id).count()+1} members'
            
            self.txt_message.bind('<Return>', lambda event, listItem= listItem: self.send_message(event,listItem))

            if self.currentItem != None:
                self.change_session_item_style(self.currentItem,self.CHAT_NORMAL)

            self.currentItem = listItem
            self.change_session_item_style(self.currentItem,self.CHAT_ACTIVE)

            if self.currentItem.dataObject.user != self.ACTIVE_USER and Container.filter(SeenMessage, SeenMessage.messageId == self.currentItem.dataObject.id,SeenMessage.seerId == DiscussionWindow.ACTIVE_USER.id).first() == None:
                Container.save(SeenMessage(date=datetime.datetime.now(),seer=DiscussionWindow.ACTIVE_USER,message=self.currentItem.dataObject))


        for li in self.msgItems:
            li.lbl_username.bind('<Button-1>', lambda event,listItem=li: Configure_session(event,listItem))

            
    def send_message(self, event, listItem):
        if self.txt_message.get() != '' and listItem != None:
            msg = Message(content=self.txt_message.get(), sentDate=datetime.datetime.now(), user=DiscussionWindow.ACTIVE_USER, session=listItem.dataObject.session)
            Container.save(msg)
            listItem.dataObject=msg
            listItem.lbl_content['text']=self.txt_message.get()
            self.txt_message.delete(0,END)
            self.fill_discussion(listItem.dataObject.session)

    # BOOKMARK_DONE: Fill chat sessions
    def fill_sessions(self):
        self.msgItems.clear()
        self.lv_sessions.empty()
        
        for i in Container.filter(Session, or_(and_(Collaboration.userId == DiscussionWindow.ACTIVE_USER.id, Session.id == Collaboration.sessionId,), Session.ownerId == DiscussionWindow.ACTIVE_USER.id)):
            msg = Container.filter(Message, Message.sessionId == i.id).order_by(Message.sentDate.desc()).first()
            if msg == None: msg = Message(content=f'welcome to the chat',user=i.owner, session=i, sentDate=i.creationDate)
            li = ListItemFactory.DiscussionListItem(self.lv_sessions.interior, msg)
            self.msgItems.append(li)
            if msg.user != self.ACTIVE_USER and Container.filter(SeenMessage, SeenMessage.messageId == msg.id,SeenMessage.seerId == DiscussionWindow.ACTIVE_USER.id).first() == None:
                self.change_session_item_style(li,self.CHAT_UNREAD)

    # BOOKMARK_DONE: Fill Messages
    def fill_discussion(self, session):
        self.lv_messages.empty()

        for i in Container.filter(Message,Message.sessionId == session.id).order_by(Message.sentDate.asc()).all():
            self.create_message(i)
            # createMethod = lambda item: DiscussionWindow.create_message_item(item, DiscussionWindow.MSG_INCOMING if i.user != DiscussionWindow.ACTIVE_USER else DiscussionWindow.MSG_OUTGOING)
            # ListItem(self.lv_messages.interior, None, 
            # {
            #     'username':i.user.userName,
            #     'content':i.content,
            #     'time': i.sentDate.strftime("%d/%m/%Y") if datetime.datetime.now().strftime("%x") != i.sentDate.strftime("%x") else i.sentDate.strftime("%X")
            # }, None, createMethod)

    def create_message(self,i):
        createMethod = lambda item: DiscussionWindow.create_message_item(item, DiscussionWindow.MSG_INCOMING if i.user != DiscussionWindow.ACTIVE_USER else DiscussionWindow.MSG_OUTGOING)
        ListItem(self.lv_messages.interior, None, 
        {
            'username':i.user.userName,
            'content':i.content,
            'time': i.sentDate.strftime("%d/%m/%Y") if datetime.datetime.now().strftime("%x") != i.sentDate.strftime("%x") else i.sentDate.strftime("%X")
        }, None, createMethod)

    # To change session list item style easily
    def change_session_item_style(self, item, style=CHAT_UNREAD):
        # Change background
        changeBgTo = [item, item.frm_content, item.lbl_username, item.lbl_content, item.lbl_time, item.img_photo]
        for w in changeBgTo:
            w.config(bg=style['bg'])
        # Change foreground
        for i in style.keys():
            if hasattr(item, i):
                getattr(item, i).config(fg=style[i])

    # Message item
    def create_message_item(item, style=MSG_INCOMING):
        hPivot = W if style == DiscussionWindow.MSG_INCOMING else E
        bubbleSize = [16, 20]
        bubbleCoords = {
            W: [(bubbleSize[0] / 2, bubbleSize[1] / 2), (bubbleSize[0], bubbleSize[1]), (0, bubbleSize[1])],
            E: [(0, 0), (bubbleSize[0], 0), (bubbleSize[0] / 2, bubbleSize[1] / 2)]
        }

        item.pack(side=TOP, anchor=N+hPivot)
        item.config(bg=background)

        bubble = Canvas(item, bg=background, width=20, height=20, highlightthickness=0)
        bubble.pack(side=(TOP if hPivot == W else BOTTOM), anchor=hPivot, padx=5)
        bubble.create_polygon(bubbleCoords[hPivot], fill=(border if hPivot == W else teal))

        frm_message = Frame(item)
        frm_message.pack(side=TOP)
        frm_message.config(padx=10, pady=10)

        frm_group = Frame(frm_message)
        frm_group.pack(side=LEFT, padx=(0, 30))

        item.lbl_username = Label(frm_group, text=item.bindings.get('username', '{username}'), font='-size 14')
        item.lbl_content = Label(frm_group, text=item.bindings.get('content', '{content}'))
        item.lbl_time = Label(frm_message, text=item.bindings.get('time', '{time}'), font='-size 8')

        item.lbl_username.pack(side=TOP, anchor=N+W)
        item.lbl_content.pack(side=TOP, anchor=N+W)
        item.lbl_time.pack(side=RIGHT, anchor=N, pady=5)

        # Change background
        changeBg = [frm_message, frm_group, item.lbl_username, item.lbl_content, item.lbl_time]
        for i in changeBg:
            i.config(bg=style['bg'])
        # Change foreground
        for i in style.keys():
            if hasattr(item, i):
                getattr(item, i).config(fg=style[i])
        # Apply a border
        if style == DiscussionWindow.MSG_INCOMING:
            frm_message.config(highlightthickness=1, highlightbackground=border)

