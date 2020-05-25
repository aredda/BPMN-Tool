from effects.transition import Transition
import time

class MoveTransition(Transition):

    def __init__(self, setter, getter, target_value, speed = 1):
        Transition.__init__(self, self.effect)

        self.setter = setter
        self.getter = getter
        self.target_value = target_value
        self.speed = speed

        self.animate()

    def effect(self):
        self.exit_time = False

        while abs(self.getter() - self.target_value) > 1:
            # Or check for exit time
            if self.exit_time == True: break
            
            self.setter ( self.getter() + (1 if self.getter() < self.target_value else -1) * self.speed )
            
            time.sleep(0.0001)