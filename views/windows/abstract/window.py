from tkinter import *
from resources.colors import *
from views.components.listitem import ListItem
from views.components.iconbutton import IconButton
from views.components.scrollable import Scrollable
from views.effects.move_transition import MoveTransition
from models.entities.Container import Container

class Window(Toplevel):
    """
    The base class of all windows in the project, this window
    shall hold all the essential and general mechanisms of a regular window.
    """

    DEFAULT_WIDTH = 1024
    DEFAULT_HEIGHT = 768

    def __init__(self, root, title='Window', width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, **args):
        Toplevel.__init__(self, root, **args)
        
        # Default configurations
        self.pack_propagate(0)
        self.grid_propagate(0)
        self.title(title)
        self.config(bg=background, width=width, height=height)
        self.center()
        
    def center(self):
        # Update the idle tasks of the window
        self.update()
        # Calculate the offset in order to center the window
        xOff = int((self.winfo_screenwidth() - self.winfo_width()) / 2)
        yOff = int((self.winfo_screenheight() - self.winfo_height()) / 2)
        # Centering the window
        self.geometry(f'{self.winfo_width()}x{self.winfo_height()}+{xOff}+{yOff}')

    def add_list_item(self, container: Scrollable, **li_args):
        """
        Takes care of instantiating a list item and then append it to the container,
        and then returns the instanciated item.
        """

        # Shrinking the finding operation
        f_arg = lambda key: li_args.get(key, None)
        # Creating an item
        li = ListItem(container, f_arg('dataObject'), f_arg('bindings'), f_arg('buttons'), f_arg('creationMethod'))
        # Appending the item
        container.pack_item(li)
        # Returning the created item
        return li

    def set_manager(self, manager):
        self.windowManager = manager

    def set_opacity(self, opacity):
        self.attributes('-alpha', opacity)

    def hide(self):
        self.withdraw() 

    def show(self):
        self.deiconify()

    def fade(self, destination=0, onFinish=None):
        MoveTransition(lambda v: self.set_opacity(v), lambda: float (self.attributes('-alpha')), destination, 0.01, 0, onFinish)

    def refresh(self):
        pass

    # Converting the position from screen world to window world
    def to_window_coords(self, screen_x, screen_y):
        return [screen_x - self.winfo_rootx(), screen_y - self.winfo_rooty()]

    def show_menu(self, **options):
        if hasattr(self, 'frm_menu') == False:
            self.frm_menu = Frame(self, bg=options.get('bg', white), width=options.get('width', 0), height=options.get('height', 0), highlightthickness=1, highlightbackground=border, padx=5, pady=5)

        # reposition menu modal
        self.frm_menu.place(x=options.get('x'), y=options.get('y'), anchor=N+E)
        # destroy children
        for child in self.frm_menu.pack_slaves():
            child.destroy()
        # fill new options
        for option in options.get('options', []):
            menu_option = IconButton(self.frm_menu, option.get('text', 'Option Text'), '-size 9 -weight bold', teal, 'resources/icons/ui/' + option.get('icon'), 14, None, teal, 28, option.get('cmnd', None), bg=white)
            menu_option.pack(side=TOP, anchor=N+W, pady=(0, (0 if options.get('options').index(option) == len(options.get('options'))-1 else 5)))


