from resources.colors import *

class Prefab:

    WIDTH = 0
    HEIGHT = 0

    LEFT_PORT = 1
    BOTTOM_PORT = 2
    RIGHT_PORT = 3
    TOP_PORT = 4

    def __init__(self, **args):
        self.id = args.get('id', [])
        self.canvas = args.get('canvas', None)
        self.element = args.get('element', None)
        self.dielement = args.get('dielement', None)

        self.parent = None
        self.flows = []
        self.unselected = []

    # necessary for finding the gui element
    def match(self, id):
        if id in self.id:
            return self
        return None

    # add the gui flow to the container
    def add_flow(self, flow):
        self.flows.append(flow) 

    # remove flow 
    def remove_flow(self, flow):
        if flow in self.flows:    
            flow.destroy()

    # draw all contained flows
    def draw_flows(self):
        for flow in self.flows:
            flow.erase()
            flow.draw()

    # clear all flows and erase them
    def unlink(self):
        for flow in self.flows:
            self.remove_flow(flow)

    # select action
    def select(self):
        for item in self.id:
            if item not in self.unselected:
                try: self.canvas.itemconfig(item, fill=selected)
                except: pass

    # deselect
    def deselect(self):
        for item in self.id:
            if item not in self.unselected:
                try: self.canvas.itemconfig(item, fill=background)
                except: pass

    # move to another position
    def move(self, x, y):
        x, y = x - self.WIDTH/2, y - self.HEIGHT/2
        # calculate the offset
        xDiff, yDiff = (x - self.x), (y - self.y)
        # move all the elements
        for id in self.id:
            oldcoords = self.canvas.coords(id)
            newcoords = []
            isX = True
            for c in oldcoords:
                newcoords.append(c + (xDiff if isX == True else yDiff))
                isX = not isX
            self.canvas.coords(id, *newcoords)
        # update the current position
        self.x, self.y = x, y
        # re draw flows
        self.draw_flows()
        # update props
        self.update_diprops()

    # necessary for zooming functionalities
    def scale(self, factor):
        self.WIDTH += factor
        self.HEIGHT += factor
        self.erase()
        self.draw()

    # used by containers only
    def resize(self, width, height):
        self.WIDTH, self.HEIGHT = width, height
        self.erase()
        self.draw()
        self.update_diprops()

    # drawing methods
    def draw(self):
        self.draw_at(self.x, self.y)
        # re drawn flows
        self.draw_flows()

    def draw_at(self, x, y):
        # updating the current position
        self.x, self.y = x, y

    def draw_text(self, text, x, y, width=0):
        # text id
        text_id = self.canvas.create_text(x, y, text=text, width=width)
        # mark as unselected item
        self.unselected.append(text_id)
        # append it to the general item list
        self.id.append(text_id)
        # redraw flows
        self.draw_flows()

    def set_text(self, text):
        self.element.name = text
        self.destroy()
        self.draw()

    # to control the z index
    def bring_front(self):
        for id in self.id:
            self.canvas.tag_raise(id)
    
    def bring_back(self):
        for id in self.id:
            self.canvas.tag_lower(id)

    # removing & erasing the gui element from the canvas
    def destroy(self):
        # delete from parent
        if self.parent != None:
            if hasattr(self.parent, 'remove_child') == True:
                self.parent.remove_child(self)
        # erase
        self.erase()
        # remove all flows
        for flow in self.flows:
            flow.destroy()

    # erasing
    def erase(self):
        # erase all drawn elements
        for id in self.id:
            self.canvas.delete(id)
        self.id.clear()
        # clear unselected list
        self.unselected.clear()

    # useful for getting commands that concerns the gui element itself
    def get_options(self):
        pass
    
    # necessary for establishing a smooth linking between elements
    def get_ports(self):
        return {
            self.LEFT_PORT: (self.x, self.y + self.HEIGHT/2),
            self.BOTTOM_PORT: (self.x + self.WIDTH/2, self.y + self.HEIGHT),
            self.RIGHT_PORT: (self.x + self.WIDTH, self.y + self.HEIGHT/2),
            self.TOP_PORT: (self.x + self.WIDTH/2, self.y)
        }

    def get_port(self, port_key):
        for key in self.get_ports().keys():
            if key == port_key:
                return self.get_ports()[port_key]
        return None

    def get_port_to(self, guielement):
        # calculate distance
        xDist, yDist = guielement.x - self.x, guielement.y - self.y
        # find the appropriate port
        port = self.BOTTOM_PORT if self.y < guielement.y else self.TOP_PORT
        if abs(xDist) > abs(yDist):
            port = self.RIGHT_PORT if self.x < guielement.x else self.LEFT_PORT
        # return 
        return [port, self.get_port(port)]

    # crucial for knowing which type of flows
    def get_process(self):
        target = self.parent
        # fetch
        while target.__class__.__name__ != 'GUIProcess' and target != None:
            target = target.parent
        # return result
        return target

    # responsible for updating di element props
    def update_diprops(self):
        if self.dielement == None:
            return
        # update reference
        self.dielement.element = self.element
        # update position
        self.dielement.bounds.x, self.dielement.bounds.y = self.x, self.y
        # update size
        self.dielement.bounds.width, self.dielement.bounds.height = self.WIDTH, self.HEIGHT
        