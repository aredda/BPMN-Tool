from views.prefabs.abstract.prefab import Prefab

class GUIContainer(Prefab):

    def __init__(self, **args):
        Prefab.__init__(self, **args)

        self.children = []

    def append_child(self, child):
        if child not in self.children:
            self.children.append(child)
    
    def move(self, x, y):
        # save previous
        xPrev, yPrev = self.x, self.y
        # call the super method
        super().move(x, y)
        # calculate distance
        xDiff, yDiff = self.x - xPrev, self.y - yPrev
        # move all children too
        for child in self.children:
            # keep the offset
            child.move(child.x + xDiff + child.WIDTH/2, child.y + yDiff + child.HEIGHT/2)
            child.bring_front()

    def draw(self):
        super().draw()
        # for each child
        for child in self.children:
            child.draw()

    def destroy(self):
        for child in self.children:
            child.destroy()
        super().destroy()