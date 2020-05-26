from views.windows.abstract.window import Window
from views.windows.abstract.sessionwindow import SessionWindow
from views.windows.abstract.tabbedwindow import TabbedWindow


def run():
    window = TabbedWindow([
        {
            'icon': 'info.png',
            'text': 'General Information',
            'tag': 'tb_info'
        },
        {
            'icon': 'history.png',
            'text': 'Histury',
            'tag': 'tb_hist'
        }
    ])
    window.mainloop()