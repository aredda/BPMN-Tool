from tkinter import * 
from resources.colors import background
from views.components.listitem import ListItem

class Scrollable(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, bg=kw.get('bg', background))            

        # create a canvas object and a vertical scrollbar for scrolling it
        self.vscrollbar = Scrollbar(self, orient=VERTICAL)
        self.vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=self.vscrollbar.set, bg=kw.get('bg', background))
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(self.canvas, **kw)
        interior_id = self.canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                self.canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', _configure_canvas)

    def empty(self):
        for child in self.interior.winfo_children():
            child.destroy()
            
        self.update()

    # Setup grid columns
    def set_gridcols(self, gridcols):
        self.gridcols = gridcols

    # Special List View Grid System
    def grid_item(self, dataObject, bindings, buttons, creationMethod=None, spacing=10, **args):
        # Initialize
        if hasattr(self, 'items') == False:
            self.lastRow = None
            self.items = []
        # Check if the last row is occupied
        if self.lastRow == None or len(self.lastRow.grid_slaves()) >= self.gridcols:
            self.lastRow = Frame(self.interior, padx=spacing, bg=self['bg'])
            self.lastRow.pack (fill=X)
            self.lastRow.rowconfigure(0, weight=1)
            self.lastRow.columnconfigure(list(range(self.gridcols)), weight=1)
        # Create the list item
        slaves_count = len(self.lastRow.grid_slaves())
        li = ListItem(self.lastRow, dataObject, bindings, buttons, creationMethod, **args)
        li.grid (row=0, column=slaves_count, padx=(0 if slaves_count == 0 else spacing, 0), pady=(0, spacing), sticky='enws')
        # Save item and update
        self.items.append(li)
        self.update()
        # Return the created item
        return li