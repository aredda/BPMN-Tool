import tkinter as tk
from tkinter import ttk
from ui.listitem import ListItem

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

        self.canvas = tk.Canvas(frame, yscrollcommand=self.scrollbar.set, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        tk.Frame.__init__(self, frame, **args)
        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)
        # Tweak configs
        self.configure(pady=self.spacing)
        self.grid_propagate(0)

    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas size"

        self.canvas.itemconfig(self.windows_item, width=event.width)        

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))

    def pack_item(self, item):
        # Pack item
        item.pack (padx=self.spacing, pady=(0 if len(self.items) > 0 else self.spacing, self.spacing))
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