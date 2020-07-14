from views.prefabs.abstract.prefab import Prefab

class GUIContainer(Prefab):

    def __init__(self, **args):
        Prefab.__init__(self, **args)

        self.children = []

    def append_child(self, child):
        if child not in self.children:
            self.children.append(child)

    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)
    
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
            if isinstance(child, GUIContainer) == True:
                for c in child.children:
                    c.bring_front()

    def draw(self):
        super().draw()
        # draw each child
        for child in self.children:
            child.draw()

    def destroy(self):
        # child disposal
        for child in self.children:
            child.destroy()
        # self destruction
        super().destroy()

    def erase(self):
        super().erase()
        # erase children
        for child in self.children:
            child.erase()