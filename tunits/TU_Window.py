from views.windows.abstract.window import Window
from views.windows.abstract.sessionwindow import SessionWindow
from views.windows.abstract.tabbedwindow import TabbedWindow
from views.windows.homewindow import HomeWindow
from views.components.scrollableframe import Scrollable
from tkinter import *
from resources.colors import *

def run():
    # window = TabbedWindow([
    #     {
    #         'icon': 'info.png',
    #         'text': 'General Information',
    #         'tag': 'tb_info'
    #     },
    #     {
    #         'icon': 'history.png',
    #         'text': 'Histury',
    #         'tag': 'tb_hist'
    #     }
    # ])
    window = HomeWindow()

    # tb1 = Frame(window.tb_container, bg=black)
    # tb2 = Frame(window.tb_container, bg=teal)

    # tb2.pack_propagate(0)
    # tb2.pack(fill=BOTH, expand=1)

    # scr = Scrollable(tb2)
    # scr.pack(fill=BOTH, expand=1)

    # window.connect_body_to('tb_info', tb1)
    # window.connect_body_to('tb_hist', tb2)

    # window.finish_tabbing()

    # print ( dir(window) )

    window.mainloop()
