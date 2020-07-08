from tkinter import Canvas
from PIL import Image as Img, ImageTk as ImgTk
from views.prefabs.abstract.prefab import Prefab

class GUIDataObject(Prefab):

    ICON_SIZE = 30
    RATIO = 1.3
    TEXT_OFFSET = 20

    def __init__(self, **args):
        super().__init__(**args)

        self.temp_text = 'Data Object'
        self.WIDTH = self.HEIGHT = self.ICON_SIZE

    def draw_at(self, x, y):
        super().draw_at(x, y)
        # draw icon
        cnv: Canvas = self.canvas
        self.icon = ImgTk.PhotoImage(Img.open('resources/icons/notation/guidataobject.png').resize((self.ICON_SIZE, int (self.ICON_SIZE * self.RATIO))))
        self.id.append(cnv.create_image(x + self.WIDTH/2, y + self.HEIGHT/2, image=self.icon))
        # draw text
        self.draw_text(self.temp_text, x + self.WIDTH/2, y + self.HEIGHT/2 - (self.ICON_SIZE/2) - self.TEXT_OFFSET)

    