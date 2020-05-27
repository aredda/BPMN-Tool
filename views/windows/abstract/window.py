from tkinter import Tk
from resources.colors import background
from views.components.listitem import ListItem
from views.components.scrollableframe import Scrollable

class Window(Tk):
    """
    The base class of all windows in the project, this window
    shall hold all the essential and general mechanisms of a regular window.
    """
    
    DEFAULT_WIDTH = 1024
    DEFAULT_HEIGHT = 768

    def __init__(self, title='Window', width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, **args):
        Tk.__init__(self, **args)

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
