from tkinter import *
from resources.colors import *
from views.windows.abstract.modal import Modal
from views.components.textbox import TextBox

class FormModal(Modal):
    
    def __init__(self, root, title, height, inputs: list, buttons: list, onCreated=None, **args):

        self.form = []

        if buttons == None: 
            buttons = []

        def correct(call, obj):
            return lambda e: call(obj)
    
        # re-configure commands
        for setting in buttons:
            if 'cmnd' in setting:
                command = setting.get('cmnd')
                setting['cmnd'] = correct(command, self)
        # add cancel button
        buttons.insert(0, {
            'text': 'Cancel',
            'icon': 'cancel.png',
            'mode': 'danger',
            'cmnd': lambda e: self.destroy()
        })

        Modal.__init__(self, root, title, buttons, self.MODAL_WIDTH, height, **args)

        # start designing
        for setting in inputs:
            frm_group = Frame(self.frm_body, bg=background)
            frm_group.pack(side=TOP, fill=X, pady=(0, 20))

            lbl_label = Label(frm_group, bg=background, fg=black, text=setting.get('label', 'Input Label'), font='-size 13 -weight bold', padx=0)
            lbl_label.pack(side=TOP, anchor=N+W, pady=(0, 5))

            txt_input = TextBox(frm_group, 'resources/icons/ui/' + setting.get('icon'))
            txt_input.pack(side=TOP, fill=X)

            self.form.append({
                'name': setting.get('name'),
                'input': txt_input,
                'getter': setting.get('getter', lambda widget: widget.get_text()) 
            })

        # after finishing the creation of the form
        if onCreated != None:
            onCreated(self)

    # Getting one input's value
    def get_form_value(self, name: str):
        for group in self.form:
            if group['name'] == name:
                return (group['getter'])(group['input'])
        return None

    # Getting the data of the whole form
    def get_form_data(self):
        data = {}
        # fetch data
        for group in self.form: data[group['name']] = self.get_form_value(group['name'])
        # return data
        return data