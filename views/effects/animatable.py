class Animatable:

    def __init__(self):
        self.bind_events ()
        self.transitions = []

    def onEnter(self):
        self.stop_transitions()
        self.clear()

    def onLeave(self):
        self.stop_transitions()
        self.clear()

    def save_transition(self, transition):
        self.transitions.append(transition)

    def stop_transitions(self):
        for t in self.transitions: t.stop()

    def clear(self):
        self.transitions.clear()

    def bind_events(self):
        self.bind ('<Enter>', lambda e: self.onEnter())
        self.bind ('<Leave>', lambda e: self.onLeave())