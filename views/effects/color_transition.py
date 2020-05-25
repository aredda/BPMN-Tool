from effects.transition import Transition
import time

class ColorTransition(Transition):

    def __init__(self, setter, getter, target_value):
        Transition.__init__(self, self.effect)

        self.setter = setter
        self.getter = getter
        self.target_value = target_value

        self.animate()

    def to_rgb(h: str):
        h = h.lstrip('#')
        return list(int(h[i:i+2], 16) for i in (0, 2, 4))

    def to_hex(rgb: list):
        return '#%02x%02x%02x' % tuple (rgb)

    def effect(self):
        time.sleep(0.05)
        
        self.exit_time = False
        timer = 0
        targetColorRgb = ColorTransition.to_rgb(self.target_value)

        while ColorTransition.to_rgb (self.getter()) != targetColorRgb:
            # If the transition took long just kill the thread
            # Or check for exit time
            if timer > 0.25 or self.exit_time == True:
                break

            currentColor = ColorTransition.to_rgb(self.getter())
            previousColor = currentColor.copy()
            
            for i in currentColor:
                j = targetColorRgb[currentColor.index(i)]
                if i != j:
                    direction = 1 if i < j else -1
                    currentColor[currentColor.index(i)] = i + direction

            self.setter (ColorTransition.to_hex(currentColor))
            time.sleep(0.001)
            timer += 0.001
