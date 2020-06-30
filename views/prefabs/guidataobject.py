from tkinter import Canvas
from PIL import Image as Img, ImageTk as ImgTk
from views.prefabs.abstract.prefab import Prefab

class GUIDataObject(Prefab):

    ICON_SIZE = 30
    RATIO = 1.3

    def __init__(self, **args):
        super().__init__(**args)

    def draw_at(self, x, y):
        super().draw_at(x, y)

        cnv: Canvas = self.canvas

        self.icon = ImgTk.PhotoImage(Img.open('resources/icons/notation/guidataobject.png').resize((self.ICON_SIZE, int (self.ICON_SIZE * self.RATIO))))
        self.id.append(cnv.create_image(x, y, image=self.icon))

    