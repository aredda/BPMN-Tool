from tkinter import *
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

from models.entities.Container import Container
from models.entities.Entities import *

from helpers.imageutility import *
from helpers.filehelper import filetobytes, bytestofile

root = None


def uploadimagefile(userid):
    if userid != 0:
        user = Container.filter(User).get(userid)
        filename = filedialog.askopenfilename(
            initialdir="/", title="select image to upload to user", filetypes=(("jpeg/jpg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")))
        if filename.lower().endswith(('.png', '.jpg')) == True:
            bytesimage = filetobytes(filename)
            user.image = bytesimage
            Container.save(user)
            image = getdisplayableimage(bytesimage, (200, 200))
            displayimage(image)
        else:
            messagebox.askokcancel(root, message='please choose an image file')
    else:
        messagebox.askokcancel(root, message='please enter a user id')


def downloadimagefile(userid):
    if userid != 0:
        user = Container.filter(User).get(userid)
        directory = filedialog.askdirectory(
            initialdir="/", title='select a directory to download the image to')
        if directory != '':
            bytestofile(directory, 'test', 'jpg', user.image)
            image = getdisplayableimage(user.image, (200, 200))
            displayimage(image)
    else:
        messagebox.askokcancel(root, message='please enter a user id')


def displayimage(image):
    global root
    label = Label(root, image=image)
    label.image = image
    label.pack()


def run():
    global root

    root = Tk()

    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    w = 800
    h = 400

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    frame = Frame(root, width=200)

    label = Label(frame, text='user\'s id : ')
    entry = Entry(frame)

    frame2 = Frame(root, width=200)

    btn_uploadImage = Button(frame2, text='open image',
                             command=lambda: uploadimagefile(int(entry.get()) if entry.get() != '' else 0))

    btn_downloadImage = Button(frame2, text='download image',
                               command=lambda: downloadimagefile(int(entry.get()) if entry.get() != '' else 0))

    label.pack(side=LEFT, padx=5, pady=5)
    entry.pack(side=RIGHT, padx=5, pady=5)

    btn_uploadImage.pack(side=LEFT, padx=5, pady=5)
    btn_downloadImage.pack(side=RIGHT, padx=5, pady=5)

    frame.pack()
    frame2.pack()

    root.mainloop()
