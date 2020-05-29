import tkinter as tk
from tkinter import ttk
from views.components.listitem import ListItem
from resources.colors import *

class Scrollable(tk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame, 
       call the update() method to refresh the scrollable area.
    """

    PACK = 0
    GRID = 1

    def __init__(self, frame, scrollBarWidth=16, spacing=10, appendMethod = PACK, columns = 2, **args):
        # Container settings
        self.spacing = spacing
        self.method = appendMethod
        self.gridcols = columns
        self.items = []
        self.lastRow = None

        self.scrollbar = tk.Scrollbar(frame, width=scrollBarWidth)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(frame, yscrollcommand=self.scrollbar.set, highlightthickness=0, bg=black, width=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.canvas.pack_forget()

        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        tk.Frame.__init__(self, frame, **args)
        # Assign this obj (the inner frame) to the windows item of the canvas
        self.window_item = self.canvas.create_window(0, 0, window=self, anchor=tk.NW)
        # Tweak configs
        self.grid_propagate(0)

        self.update()

    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas size"

        self.canvas.itemconfig(self.window_item, width=event.width)        

    def update(self):
        "Update the canvas and the scrollregion"
        self.update_idletasks()
        region = self.canvas.bbox(all)
        self.canvas.config(scrollregion=region)

    def pack_item(self, item, **args):
        # Default args
        defArgs = {'padx':self.spacing, 'pady':(0, self.spacing)}
        # Override default ones
        if args is None:
            args = defArgs
        # Pack item
        item.pack (**args)
        # Save item
        self.items.append (item)
        # Update
        self.update()

    def grid_item(self, dataObject, bindings, buttons, creationMethod=None, **args):
        # Check if the last row is occupied
        if self.lastRow == None or len(self.lastRow.grid_slaves()) >= self.gridcols:
            self.lastRow = tk.Frame(self, padx=self.spacing, bg=self['bg'])
            self.lastRow.pack (fill=tk.X)
            self.lastRow.rowconfigure(0, weight=1)
            self.lastRow.columnconfigure(list(range(self.gridcols)), weight=1)
        # Create the list item
        slaves_count = len(self.lastRow.grid_slaves())
        li = ListItem(self.lastRow, dataObject, bindings, buttons, creationMethod, **args)
        li.grid (row=0, column=slaves_count, padx=(0 if slaves_count == 0 else self.spacing, 0), pady=(0, self.spacing), sticky='enws')
        # Save item and update
        self.items.append(li)
        self.update()
        # Return the created item
        return li

    def empty(self):
        for child in self.winfo_children():
            child.destroy()
        self.items.clear()
        self.update()