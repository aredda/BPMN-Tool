class Prefab:
    
    def __init__(self, **args):
        # abstract fields
        self.id = args.get('id', [])
        self.canvas = args.get('canvas', None)
        self.element = args.get('element', None)
        self.dielement = args.get('dielement', None)

    def move(self, x, y):
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

    def scale(self, factor):
        pass

    def resize(self, width, height):
        pass

    def draw(self):
        pass

    def draw_at(self, x, y):
        # updating the current position
        self.x, self.y = x, y

    def bring_front(self):
        for id in self.id:
            self.canvas.tag_raise(id)
    
    def bring_back(self):
        for id in self.id:
            self.canvas.tag_lower(id)

    def destroy(self):
        # remove all drawn elements
        for id in self.id:
            self.canvas.delete(id)