from tkinter import *
from resources.colors import *
from views.factories.iconbuttonfactory import MainButton, SecondaryButton, DangerButton
from views.components.textbox import TextBox
from views.windows.abstract.window import Window

class SignWindow(Window):

    def __init__(self, root):
        super().__init__(root, 'BPMN Tool')

        self.design()

    def design(self):
        # lay out the container frames
        self.frm_in = Frame(self, bg=background, width=self.DEFAULT_WIDTH/2, padx=100)
        self.frm_in.pack(side=RIGHT, expand=1, fill=BOTH)
        self.frm_up = Frame(self, bg=background, width=self.DEFAULT_WIDTH/2, padx=100)
        self.frm_up.pack(side=LEFT, expand=1, fill=BOTH)
        self.frm_in.pack_propagate(0)
        self.frm_up.pack_propagate(0)
        # design the sign in side
        self.lbl_title_signin = Label(self.frm_in, text='Sign in', fg=teal, bg=background, font='-size 32 -weight bold')
        self.lbl_title_signin.pack(side=TOP, pady=(150, 50))
        signin_config = [
            { 'name': 'txt_in_username', 'label': 'Username:', 'icon': 'account.png' },
            { 'name': 'txt_in_password', 'label': 'Password:', 'icon': 'key.png' }
        ]
        # put the form in place
        for config in signin_config:
            Label(self.frm_in, text=config.get('label'), font='-size 11 -weight bold', fg=black, bg=background).pack(side=TOP, anchor=N+W, pady=(0, 5))
            tb = TextBox(self.frm_in, 'resources/icons/ui/' + config.get('icon'))
            tb.pack(side=TOP, fill=X, anchor=N+W, pady=(0, 10))
            setattr(self, config.get('name'), tb)
        # buttons
        frm_in_btns = Frame(self.frm_in, bg=background)
        frm_in_btns.pack(side=TOP, fill=X, pady=(5, 0))
        self.btn_signin = MainButton(frm_in_btns, 'Sign in', 'login.png', self.btn_signin_click)
        self.btn_signin.pack(side=LEFT)
        self.btn_viewpwd = SecondaryButton(frm_in_btns, 'View Password', 'eye.png', self.btn_viewpassword_click)
        self.btn_viewpwd.pack(side=RIGHT)
        # divider
        frm_in_divider = Frame(self.frm_in, bg=border)
        frm_in_divider.pack(side=TOP, fill=X, pady=(100, 5))
        # extra options frame
        frm_in_xtra = Frame(self.frm_in, bg=background)
        frm_in_xtra.pack(side=TOP, fill=X)
        self.lbl_signup = Label(frm_in_xtra, fg=teal, font='-size 9', text='Sign up', bg=background)
        self.lbl_signup.pack(side=RIGHT)
        self.lbl_signup.bind('<Button-1>', self.lbl_signup_click)
        self.lbl_forgotpwd = Label(frm_in_xtra, fg=black, font='-size 9 -underline 1', text='Forgot your password?', bg=background)
        self.lbl_forgotpwd.pack(side=LEFT)
        self.lbl_forgotpwd.bind('<Button-1>', self.lbl_forgotpwd_click)
        # designing the sign up side
        up_congig = {
            'Step 1: Authentication Settings': [
                { 'name': 'txt_email', 'label': 'Email:', 'icon': 'mail.png' },
                { 'name': 'txt_up_pwd', 'label': 'Password:', 'icon': 'key.png' },
                { 'name': 'txt_confirm', 'label': 'Confirm Password:', 'icon': 'key.png' }
            ],
            'Step 2: Identity Information': [
                { 'name': 'txt_up_username', 'label': 'Username:', 'icon': 'account.png' },
                { 'name': 'txt_firstname', 'label': 'First Name:', 'icon': 'account.png' },
                { 'name': 'txt_lastname', 'label': 'Last Name:', 'icon': 'account.png' }
            ],
            'Step 3: Personal Information': [
                { 'name': 'txt_gender', 'label': 'Gender:', 'icon': 'wc.png' },
                { 'name': 'txt_company', 'label': 'Company:', 'icon': 'business.png' },
                { 'name': 'txt_lastname', 'label': 'Last Name:', 'icon': 'account.png' }
            ]
        }
        # preparations
        self.steptitles = []
        self.checkpoints = []
        self.forms = []
        # sign up header
        self.lbl_title_signup = Label(self.frm_up, text='Sign Up', fg=teal, bg=background, font='-size 32 -weight bold')
        self.lbl_title_signup.pack(side=TOP, pady=(100, 50))
        # step label
        self.lbl_step = Label(self.frm_up, text='Step X: Description', fg=black, bg=background, font='-size 12')
        self.lbl_step.pack(side=TOP)
        # map frame
        self.frm_map = Frame(self.frm_up, bg=background)
        self.frm_map.pack(side=TOP, fill=X, pady=(5, 0))
        for s in up_congig.keys():
            frm_cp = Frame(self.frm_map, highlightthickness=1, highlightbackground=border, height=15, bg=white)
            frm_cp.pack(side=LEFT, fill=X, expand=1, padx=(0, 4 if list(up_congig.keys()).index(s) != len(up_congig.keys()) else 0))
            self.checkpoints.append(frm_cp)
        # forms container
        self.frm_frmcontainer = Frame(self.frm_up, bg=background)
        self.frm_frmcontainer.pack(side=TOP, fill=X, pady=(30, 0))
        for s in up_congig.keys():
            tb_config = up_congig.get(s)
            frm_form = Frame(self.frm_frmcontainer, bg=background)
            for i in tb_config:
                Label(frm_form, text=i.get('label'), font='-size 11 -weight bold', fg=black, bg=background).pack(side=TOP, anchor=N+W, pady=(0, 5))
                tb = TextBox(frm_form, 'resources/icons/ui/' + i.get('icon'))
                tb.pack(side=TOP, fill=X, anchor=N+W, pady=(0, 10))
                setattr(self, i.get('name'), tb)
            # save those entities
            self.steptitles.append(s)
            self.forms.append(frm_form)
        # display the first step
        self.move_to(0)

    def move_to(self, index: int):
        # change the label's text
        self.lbl_step.config(text=self.steptitles[index])
        # show the corresponding form container
        for frm in self.forms: frm.pack_forget()
        self.forms[index].pack(side=TOP, fill=X)

    # BOOKMARK: Sign In Logic
    def btn_signin_click(self, event):
        print ('Sign In Command is not implemented')

    # BOOKMARK: View Password Logic
    def btn_viewpassword_click(self, event):
        print ('View Password Command is not implemented')

    # BOOKMARK: Sign Up Next
    def btn_signup_next(self, event):
        print ('Next Command is not implemented')

    # BOOKMARK: Go to Sign Up Form
    def lbl_signup_click(self, event):
        print ('Sign up form is requested..')

    # BOOKMARK: Forgotten password
    def lbl_forgotpwd_click(self, event):
        pass