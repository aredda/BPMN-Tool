from tkinter import *
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

from models.entities.Container import Container
from models.entities.Entities import *

from helpers.xmlutility import *
from helpers.filehelper import filetobytes, bytestofile

root = None


def uploadxmlfile(projectid):
    if projectid != 0:
        project = Container.filter(Project).get(projectid)
        filename = filedialog.askopenfilename(
            initialdir="/", title="select xml file to upload to project", filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
        if filename.lower().endswith('.xml') == True:
            bytesfile = filetobytes(filename)
            if len(bytesfile) != 0:
                project.file = bytesfile
                Container.save(project)
                element = bytestoelement(bytesfile)
                displaycontent(element)
            else:
                messagebox.showwarning(root, message='Empty xml file')
        else:
            messagebox.askokcancel(root, message='please choose an xml file')
    else:
        messagebox.askokcancel(root, message='please enter a project id')


def downloadxmlfile(projectid):
    if projectid != 0:
        project = Container.filter(Project).get(projectid)
        directory = filedialog.askdirectory(
            initialdir="/", title='select a directory to download the xml file to')
        if directory != '':
            bytestofile(directory, 'testxml', 'xml', project.file)
            element = bytestoelement(project.file)
            displaycontent(element)
    else:
        messagebox.askokcancel(root, message='please enter a project id')


def displaycontent(element):
    global root
    label = Label(root, justify=LEFT, text=ET.tostring(element))
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

    label = Label(frame, text='project\'s id : ')
    entry = Entry(frame)

    frame2 = Frame(root, width=200)

    btn_uploadxmlfile = Button(frame2, text='upload xml file',
                               command=lambda: uploadxmlfile(int(entry.get()) if entry.get() != '' else 0))

    btn_downloadxmlfile = Button(frame2, text='download xml file',
                                 command=lambda: downloadxmlfile(int(entry.get()) if entry.get() != '' else 0))

    label.pack(side=LEFT, padx=5, pady=5)
    entry.pack(side=RIGHT, padx=5, pady=5)

    btn_uploadxmlfile.pack(side=LEFT, padx=5, pady=5)
    btn_downloadxmlfile.pack(side=RIGHT, padx=5, pady=5)

    frame.pack()
    frame2.pack()

    root.mainloop()
