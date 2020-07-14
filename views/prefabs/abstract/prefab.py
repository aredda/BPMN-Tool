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

    # necessary for finding the gui element
    def match(self, id):
        if id in self.id:
            return self
        return None

    # add the gui flow to the container
    def add_flow(self, flow):
        self.flows.append(flow)

    # draw all contained flows
    def draw_flows(self):
        for flow in self.flows:
            flow.destroy()
            flow.draw()

    # clear all flows and erase them
    def unlink(self):
        for flow in self.flows:
            for ref in [flow.guisource, flow.guitarget]:
                if ref != flow:
                    ref.flows.remove(flow)
        self.flows.clear()

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

    # drawing methods
    def draw(self):
        self.draw_at(self.x, self.y)
        # re drawn flows
        for flow in self.flows:
            flow.draw()

    def draw_at(self, x, y):
        # updating the current position
        self.x, self.y = x, y

    def draw_text(self, text, x, y, width=0):
        self.id.append(self.canvas.create_text(x, y, text=text, width=width))
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
        