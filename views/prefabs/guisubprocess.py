from tkinter import Canvas
from PIL import Image as img, ImageTk as imgTk
from resources.colors import *
from views.prefabs.guiactivity import GUIActivity
from views.prefabs.abstract.guicontainer import GUIContainer

class GUISubProcess(GUIActivity, GUIContainer):

    TEXT_OFFSET_Y = 16

    def __init__(self, **args):
        GUIActivity.__init__(self, **args)
        GUIContainer.__init__(self, **args)
        # default size
        self.WIDTH = 250
        self.HEIGHT = 200

        self.temp_text = 'Sub-Process'

    def draw_at(self, x, y):
        # draw the border
        GUIActivity.draw_at(self, x, y)
        # draw collapsed subprocess icon
        iconpath = 'resources/icons/notation/collapsedsubprocess.png'
        self.type_icon = imgTk.PhotoImage(img.open(iconpath).resize((self.ICON_SIZE, self.ICON_SIZE)))
        cnv: Canvas = self.canvas
        self.id.append (cnv.create_image(x + (self.WIDTH / 2) + (self.ICON_MARGIN / 4) + (self.ICON_SIZE / 2), y + self.HEIGHT - self.ICON_MARGIN, image=self.type_icon))
        # draw text
        self.draw_text(self.temp_text, x + self.WIDTH/2, y - self.TEXT_OFFSET_Y)

    def move(self, x, y):
        GUIContainer.move(self, x, y)