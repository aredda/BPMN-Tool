from tkinter import Canvas
from PIL import Image as Img, ImageTk as ImgTk
from views.prefabs.abstract.prefab import Prefab

class GUIDataStore(Prefab):

    ICON_SIZE = 50
    TEXT_OFFSET = 16

    def __init__(self, **args):
        super().__init__(**args)

        self.temp_text = 'Data Store'

    def draw_at(self, x, y):
        super().draw_at(x, y)
        # draw icon
        cnv: Canvas = self.canvas
        self.icon = ImgTk.PhotoImage(Img.open('resources/icons/notation/guidatastore.png').resize((self.ICON_SIZE, self.ICON_SIZE)))
        self.id.append(cnv.create_image(x, y, image=self.icon))
        # draw text
        self.draw_text(self.temp_text, x, y - (self.ICON_SIZE/2) - self.TEXT_OFFSET)

    