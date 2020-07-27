from tkinter import Canvas
from PIL import Image as img, ImageTk as imgTk
from resources.colors import *
from views.prefabs.abstract.guilinkable import GUILinkable
from models.bpmn.enums.activityflag import ActivityFlag
from models.bpmndi.shape import BPMNShape
from models.bpmndi.bounds import Bounds

class GUIActivity(GUILinkable):
    
    RADIUS = 10

    ICON_MARGIN = 16
    ICON_SIZE = 26

    def __init__(self, **args):
        GUILinkable.__init__(self, **args)

        self.WIDTH = 150
        self.HEIGHT = 100

        self.dielement = args.get('dielement', BPMNShape())

        if self.dielement.bounds == None:
            self.dielement.bounds = Bounds()

    def draw_at(self, x, y):
        GUILinkable.draw_at(self, x, y)
        # extract info
        flag = self.element.flag
        # get canvas
        cnv: Canvas = self.canvas
        # border points
        points = [
            x+self.RADIUS, y,
            x+self.RADIUS, y,
            x + self.WIDTH-self.RADIUS, y,
            x + self.WIDTH-self.RADIUS, y,
            x + self.WIDTH, y,
            x + self.WIDTH, y+self.RADIUS,
            x + self.WIDTH, y+self.RADIUS,
            x + self.WIDTH, y + self.HEIGHT-self.RADIUS,
            x + self.WIDTH, y + self.HEIGHT-self.RADIUS,
            x + self.WIDTH, y + self.HEIGHT,
            x + self.WIDTH-self.RADIUS, y + self.HEIGHT,
            x + self.WIDTH-self.RADIUS, y + self.HEIGHT,
            x+self.RADIUS, y + self.HEIGHT,
            x+self.RADIUS, y + self.HEIGHT,
            x, y + self.HEIGHT,
            x, y + self.HEIGHT-self.RADIUS,
            x, y + self.HEIGHT-self.RADIUS,
            x, y+self.RADIUS,
            x, y+self.RADIUS,
            x, y
        ]
        # draw border
        self.id.append (cnv.create_polygon(points, fill=cnv['bg'], width=2, outline=black, smooth=True))
        # draw flag icon
        if flag != ActivityFlag.Default:
            iconpath = str(flag).lower().split('.')[1]
            if 'multiple' in iconpath: iconpath = 'parallelinstance'
            self.flag_icon = imgTk.PhotoImage(img.open('resources/icons/notation/' + iconpath + '.png').resize((self.ICON_SIZE, self.ICON_SIZE)))
            # adjusting coords of the icon depending on the element
            flag_x = x + self.WIDTH / 2
            if self.__class__.__name__ == 'GUISubProcess':
                flag_x -= self.ICON_MARGIN / 4
            self.id.append (cnv.create_image(flag_x, y + self.HEIGHT - self.ICON_MARGIN, image=self.flag_icon))

    def get_options(self):
        optlist = []

        def corrector(flag):
            return lambda e: self.set_flag(flag)

        for f in list(ActivityFlag):
            fstr = str(f).split('.')[1]
            optlist.append({
                'folder': 'resources/icons/notation/',
                'icon': (('parallelinstance' if f in [ActivityFlag.ParallelMultiple, ActivityFlag.SequentialMultiple] else (fstr.lower() if f != ActivityFlag.Default else 'task'))) + '.png',
                'text': f'Flag as {fstr}',
                'fg': gray1,
                'textfg': gray,
                'cmnd': corrector(f)
            })

        return optlist
        
    def set_flag(self, flag):
        self.element.flag = flag
        self.destroy()
        self.draw()

    def scale(self, factor):
        # conditions
        if factor < 0 and self.ICON_SIZE < factor:
            return
        # adjust
        self.ICON_SIZE += factor
        self.ICON_MARGIN += factor/2
        # refresh
        super().scale(factor)