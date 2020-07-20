from tkinter import *
from PIL import Image as Img, ImageTk as ImgTk
from resources.colors import *
from views.components.icon import IconFrame
from views.windows.abstract.window import Window

class SplashWindow(Window):

    def __init__(self, root):
        super().__init__(root, 'BPMN Tool')

        self.design()

    def design(self):
        # lay out the abstract art
        self.ref_img_art = ImgTk.PhotoImage(Img.open('resources/graphics/splash_art.png'))
        self.img_art = Label(self, image=self.ref_img_art, bg=background, width=self.ref_img_art.width()-6)
        self.img_art.pack(side=LEFT, fill=BOTH)
        # lay out the content frame
        self.frm_container = Frame(self, bg=background)
        self.frm_container.pack(side=LEFT, fill=BOTH, expand=1, pady=(250, 0))
        # headers frame
        self.frm_headers = Frame(self.frm_container, bg=background)
        self.frm_headers.pack(side=TOP)
        # BPMN TOOL label
        self.lbl_h1 = Label(self.frm_headers, text='BPMN Tool', fg=teal, bg=background, font='-size 42 -weight bold')
        self.lbl_h1.pack(side=TOP)
        # Description Label
        self.lbl_desc = Label(self.frm_headers, text='A desktop solution for BPMN modeling', bg=background, fg=black, font='size -17')
        self.lbl_desc.pack(side=TOP)
        # credits frame
        self.frm_credits = Frame(self.frm_container, bg=background)
        self.frm_credits.pack(side=TOP, pady=(100, 25))
        # Developed by label
        self.lbl_by = Label(self.frm_credits, text='Developed By:', bg=background, fg=teal, font='-weight bold -size 11')
        self.lbl_by.pack(side=TOP)
        # names
        self.lbl_names = Label(self.frm_credits, text='Ibrahim Areda, Mohamed Kalai', bg=background, fg=black)
        self.lbl_names.pack(side=TOP)
        # bottom frame
        self.frm_bottom = Frame(self.frm_container, bg=background)
        self.frm_bottom.pack(side=TOP, fill=X, padx=50)
        # bottom labels frame
        self.frm_btm_lbls = Frame(self.frm_bottom, bg=background)
        self.frm_btm_lbls.pack(side=TOP, fill=X)
        # Loading... label
        self.lbl_loading = Label(self.frm_btm_lbls, text='Loading...', fg=black, bg=background, font='-size 12')
        self.lbl_loading.pack(side=LEFT)
        # Progress label
        self.lbl_progress = Label(self.frm_btm_lbls, text='5%', fg=teal, bg=background, font='-size 12 -weight bold')
        self.lbl_progress.pack(side=RIGHT)
        # progress bar
        self.frm_bar = Frame(self.frm_bottom, bg=white, highlightthickness=2, highlightbackground=teal)
        self.frm_bar.pack(side=BOTTOM, fill=X, pady=(5, 0))
        self.frm_filler = Frame(self.frm_bar, bg=teal, height=10, width=10)
        self.frm_filler.pack(side=LEFT)
