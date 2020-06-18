class Prefab:
    
    def __init__(self, **args):
        # abstract fields
        self.id = args.get('id', None)
        self.canvas = args.get('canvas', None)
        self.element = args.get('element', None)
        self.dielement = args.get('dielement', None)

    def move(self, x, y):
        pass

    def scale(self, factor):
        pass

    def resize(self, width, height):
        pass

    def draw(self):
        pass