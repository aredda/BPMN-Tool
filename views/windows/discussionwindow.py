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

    # # Chat Session Item Styles
    # CHAT_NORMAL = {
    #     'bg': white,
    #     'lbl_username': teal,
    #     'lbl_content': black,
    #     'lbl_time': gray 
    # }
    # CHAT_UNREAD = {
    #     'bg': background,
    #     'lbl_username': teal,
    #     'lbl_content': black,
    #     'lbl_time': gray 
    # }
    CHAT_ACTIVE = {
        'bg': teal,
        'lbl_username': background,
        'lbl_user': white,
        'lbl_content': white,
        'lbl_time': white 
    }

    # Message Item Styles
    MSG_INCOMING = SessionWindow.CHAT_NORMAL
    MSG_OUTGOING = CHAT_ACTIVE

    def __init__(self, root, **args):
        SessionWindow.__init__(self, root, 'Discussions')
        
        self.currentItem = None
        self.msgItems = []

        self.design()
        self.fill_sessions()

        if args.get('session', None) != None: 
            for li in self.msgItems:
                if li.dataObject.session == args['session']:
                    self.Configure_session(None, li)
                    break

    def design(self):
        # Session items section
        self.frm_body.config(padx=0, pady=0)

        frm_sessions = Frame(self.frm_body, bg=background, width=300)
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

        self.is_hint_deleted = False
        self.txt_message = Entry(frm_footer, highlightthickness=0, relief=FLAT, font='-size 12', fg=black)
        self.txt_message.insert(0, 'Type your message here...')
        self.txt_message.pack(side=LEFT, fill=BOTH, expand=1)

        def txt_message_focus(e):
            self.is_hint_deleted = True
            self.txt_message.delete(0, len(self.txt_message.get()))

        self.txt_message.bind('<FocusIn>', txt_message_focus)

        IconFrame(frm_footer, 'resources/icons/ui/send.png', 25, teal,command=lambda event: self.send_message(event,self.currentItem)).pack(side=RIGHT)

        frm_border_top = Frame(frm_discussion, highlightthickness=1, highlightbackground=border)
        frm_border_top.pack(side=BOTTOM, fill=X)

        self.frm_veil = Frame(frm_discussion, bg=background)
        self.frm_veil.place(relwidth=1, relheight=1, x=0, y=0)

    def runnable2(self):
        # try:
            while self.time_to_kill != True:
                time.sleep(2)
                # Container.session.commit()
                for li in self.msgItems:
                    lastmsg = Container.filter(Message, Message.sessionId == li.dataObject.session.id).order_by(Message.sentDate.desc()).first()
                    if lastmsg != None and lastmsg != li.dataObject:
                        li.lbl_content['text'] = lastmsg.content if len (lastmsg.content) < 20 else lastmsg.content[:17] + '...'
                        li.lbl_time['text'] = lastmsg.sentDate.strftime("%X")
                        li.dataObject = lastmsg
                        self.change_session_item_style(li,self.CHAT_UNREAD)
                        if self.currentItem != None and self.currentItem == li: 
                            self.currentItem = li
                            self.create_message(lastmsg)
        # except Exception:
        #     # Container.session.rollback()
        #     print('RUNNABLE2 ERROR')
        
    def hide(self):
        # thread killer logic will be here
        self.time_to_kill = True
        # continute the original work
        super().hide()

    def refresh(self):
        super().refresh()
        self.time_to_kill = False
        # start thread
        threading.Thread(target=self.runnable2).start()

    def open_session(self, event):
        if self.currentItem != None:
            self.windowManager.run(CollaborationWindow(self,self.currentItem.dataObject.session))

    def Configure_session(self, event, listItem):
        self.frm_veil.place_forget()

        self.fill_discussion(listItem.dataObject.session)

        self.lbl_sessionName['text'] = listItem.dataObject.session.title
        self.lbl_memberCount['text'] = f'{Container.filter(Collaboration,Collaboration.sessionId == listItem.dataObject.session.id).count()+1} members'
        
        self.txt_message.bind('<Return>', lambda event, listItem= listItem: self.send_message(event,listItem))

        if self.currentItem != None:
            self.change_session_item_style(self.currentItem, self.CHAT_NORMAL)

        self.currentItem = listItem
        self.change_session_item_style(self.currentItem, self.CHAT_ACTIVE)

        # lastmsg = Container.filter(Message, Message.sessionId == self.currentItem.dataObject.session.id, Message.sentDate == Container.filter(func.max(Message.sentDate), Message.sessionId == self.currentItem.dataObject.session.id).group_by(Message.sessionId)).first()
        lastmsg = Container.filter(Message, Message.sessionId == self.currentItem.dataObject.session.id).order_by(Message.sentDate.desc()).first()
    
        if self.currentItem.dataObject.user != self.ACTIVE_USER and Container.filter(SeenMessage, SeenMessage.messageId == lastmsg.id,SeenMessage.seerId == DiscussionWindow.ACTIVE_USER.id).first() == None:
            Container.save(SeenMessage(date=datetime.datetime.now(),seer=DiscussionWindow.ACTIVE_USER,message=lastmsg))

    # Configure sessionlistitem click event
    def configure_session_click(self):
        for li in self.msgItems:
            for control in [li, li.lbl_username, li.img_photo, li.frm_content, li.lbl_user, li.lbl_content, li.lbl_time]:
                control.bind('<Button-1>', lambda event, listItem=li: self.Configure_session(event, listItem))
                # control.bind('<Button-1>', lambda e: print ('haha'))
            
    def send_message(self, event, listItem):
        if self.txt_message.get() != '' and not str.isspace(self.txt_message.get()) and listItem != None and self.is_hint_deleted == True:
            msg = Message(content=self.txt_message.get(), sentDate=datetime.datetime.now(), user=DiscussionWindow.ACTIVE_USER, session=listItem.dataObject.session)
            Container.save(msg)
            listItem.dataObject=msg
            listItem.lbl_content['text'] = self.txt_message.get() if len(self.txt_message.get()) < 20 else (self.txt_message.get()[:17] + '...')
            self.txt_message.delete(0, END)
            self.fill_discussion(listItem.dataObject.session)

    # BOOKMARK_DONE: Fill chat sessions
    def fill_sessions(self):
        self.msgItems.clear()
        self.lv_sessions.empty()
        
        for i in Container.filter(Session):
            if i.owner == DiscussionWindow.ACTIVE_USER or Container.filter(Collaboration, Collaboration.userId == DiscussionWindow.ACTIVE_USER.id, Collaboration.sessionId == i.id).first() != None:
                msg = Container.filter(Message, Message.sessionId == i.id).order_by(Message.sentDate.desc()).first()
                # if msg == None: msg = Message(content=f'welcome to the chat',user=i.owner, session=i, sentDate=i.creationDate)
                li = ListItemFactory.DiscussionListItem(self.lv_sessions.interior, msg)
                self.msgItems.append(li)
                if msg.user != self.ACTIVE_USER and Container.filter(SeenMessage, SeenMessage.messageId == msg.id,SeenMessage.seerId == DiscussionWindow.ACTIVE_USER.id).first() == None:
                    self.change_session_item_style(li,self.CHAT_UNREAD)
                # append to a static a list
        # configure item click
        self.configure_session_click()

    # BOOKMARK_DONE: Fill Messages
    def fill_discussion(self, session):
        # dispose of old items
        self.lv_messages.empty()
        # fill with new items
        for i in Container.filter(Message,Message.sessionId == session.id).order_by(Message.sentDate.asc()).all():
            self.create_message(i)
        # scroll up
        self.lv_messages.canvas.yview_moveto(0)
        # scrolling down thread
        def scroll_down_thread():
            # import sleep method
            from time import sleep
            # sleep for a while
            sleep (0.25)
            # scroll down
            self.lv_messages.canvas.yview_moveto(1)
        # start thread
        threading.Thread(target=scroll_down_thread).start()


    def create_message(self,i):
        createMethod = lambda item: DiscussionWindow.create_message_item(item, DiscussionWindow.MSG_INCOMING if i.user != DiscussionWindow.ACTIVE_USER else DiscussionWindow.MSG_OUTGOING)
        return ListItem(self.lv_messages.interior, None, 
        {
            'username':i.user.userName,
            'content':i.content,
            'time': i.sentDate.strftime("%d/%m/%Y") if datetime.datetime.now().strftime("%x") != i.sentDate.strftime("%x") else i.sentDate.strftime("%X")
        }, None, createMethod)


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
        item.lbl_content = Label(frm_group, wraplength=500, justify='left', text=item.bindings.get('content', '{content}'))
        item.lbl_time = Label(frm_message, text=item.bindings.get('time', '{time}'), font='-size 8')

        item.lbl_username.pack(side=TOP, anchor=N+W)
        item.lbl_content.pack(side=TOP, anchor=N+W)
        item.lbl_time.pack(side=RIGHT, anchor=N, pady=5)

        # Change background
        for i in [frm_message, frm_group, item.lbl_username, item.lbl_content, item.lbl_time]:
            i.config(bg=style['bg'])
        # Change foreground
        for i in style.keys():
            if hasattr(item, i):
                getattr(item, i).config(fg=style[i])
        # Apply a border
        if style == DiscussionWindow.MSG_INCOMING:
            frm_message.config(highlightthickness=1, highlightbackground=border)

