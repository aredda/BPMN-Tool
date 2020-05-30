from views.effects.transition import Transition
import time

class MoveTransition(Transition):

    def __init__(self, setter, getter, target_value, speed = 1, dist=1, onFinish=None):
        Transition.__init__(self, self.effect)

        self.setter = setter
        self.getter = getter
        self.target_value = target_value
        self.speed = speed
        self.dist = dist
        self.onFinish = onFinish

        self.animate()

    def effect(self):
        self.exit_time = False

        while abs(self.getter() - self.target_value) > self.dist:
            # Or check for exit time
            if self.exit_time == True: break
            # Approach
            self.setter ( self.getter() + (1 if self.getter() < self.target_value else -1) * self.speed )
            # Wait
            time.sleep(0.0001)

        if self.onFinish != None:
            self.onFinish()