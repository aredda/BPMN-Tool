from views.prefabs.abstract.prefab import Prefab

class GUILinkable(Prefab):

    def __init__(self, **args):
        Prefab.__init__(self, **args)

        self.flows = []

    def add_flow(self, flow):
        self.flows.append(flow)

    def move(self, x, y):
        super().move(x, y)
        self.draw_flows()

    def draw_at(self, x, y):
        super().draw_at(x, y)
        self.draw_flows()

    def destroy(self):
        for flow in self.flows:
            flow.destroy()
        self.flows.clear()
        super().destroy()

    def draw_flows(self):
        for flow in self.flows:
            flow.destroy()
            flow.draw()