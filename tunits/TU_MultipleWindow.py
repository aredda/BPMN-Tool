from tkinter import *

def run():

    root = Tk()
    root.withdraw()

    win1 = Toplevel(root)
    win2 = Toplevel(root)

    def btn_go_to():
        win1.withdraw()
        win2.deiconify()

    Label(win1, text='window 1').pack()
    Button(win1, text='To Win 2', command=btn_go_to).pack()
    
    Label(win2, text='window 2').pack()
    Button(win2, text='Return')

    win2.withdraw()

    root.mainloop()