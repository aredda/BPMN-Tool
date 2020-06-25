from tkinter import Canvas
from PIL import Image as img, ImageTk as imgTk
from resources.colors import *
from views.prefabs.abstract.guilinkable import GUILinkable
from models.bpmn.enums.activityflag import ActivityFlag

class GUIActivity(GUILinkable):
    
    WIDTH = 150
    HEIGHT = 100
    RADIUS = 10

    ICON_MARGIN = 16
    ICON_SIZE = 26

    def __init__(self, **args):
        GUILinkable.__init__(self, **args)

    def draw_at(self, x, y):
        GUILinkable.draw_at(self, x, y)
        # extract info
        flag = ActivityFlag.Loop
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
            if 'multiple' in iconpath: iconpath = 'parallel'
            self.flag_icon = imgTk.PhotoImage(img.open('resources/icons/notation/' + iconpath + '.png').resize((self.ICON_SIZE, self.ICON_SIZE)))
            # adjusting coords of the icon depending on the element
            flag_x = x + self.WIDTH / 2
            if self.__class__.__name__ == 'GUISubProcess':
                flag_x -= self.ICON_MARGIN / 4
            self.id.append (cnv.create_image(flag_x, y + self.HEIGHT - self.ICON_MARGIN, image=self.flag_icon))

    def move(self, x, y):
        GUILinkable.move(self, x - (self.WIDTH/2), y - (self.HEIGHT/2))
        
