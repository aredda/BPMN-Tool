from views.prefabs.abstract.prefab import Prefab

class GUIContainer(Prefab):

    def __init__(self, **args):
        Prefab.__init__(self, **args)

        self.children = []

    def append_child(self, child):
        if child not in self.children:
            # set parent
            child.parent = self
            # append in the list of gui children
            self.children.append(child)
            # append in the list of model children
            self.element.add(child.element.get_tag(), child.element)
            # add those flows
            self.register_flows(child)

    def remove_child(self, child):
        if child in self.children:
            # deny child
            child.parent = None
            # remove it from collection
            self.children.remove(child)
            # remove it from model collection
            self.element.remove(child.element.get_tag(), child.element)
            # remove its flows
            self.unregister_flows(child)
    
    # responsible for registering sequence flows in the container in order to serialize them
    def register_flows(self, child):
        for flow in child.flows:
            # skip message flows
            if flow.element.get_tag() == 'sequenceflow':
                # add this element to
                self.element.add('flow', flow.element)
    
    # unregister flows
    def unregister_flows(self, child):
        for flow in child.flows:
            if flow.element.get_tag() == 'sequenceflow':
                self.element.remove('flow', flow.element)

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