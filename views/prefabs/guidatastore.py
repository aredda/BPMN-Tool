from tkinter import Canvas
from PIL import Image as Img, ImageTk as ImgTk
from views.prefabs.abstract.prefab import Prefab
from models.bpmn.datastorereference import DataStoreReference
from models.bpmndi.shape import BPMNShape

class GUIDataStore(Prefab):

    ICON_SIZE = 50
    TEXT_OFFSET = 16

    def __init__(self, **args):
        super().__init__(**args)

        self.element = args.get('element', DataStoreReference())
        self.dielement = args.get('dielement', BPMNShape())

        self.WIDTH = self.HEIGHT = self.ICON_SIZE

    def draw_at(self, x, y):
        super().draw_at(x, y)
        cnv: Canvas = self.canvas
        self.icon = ImgTk.PhotoImage(Img.open('resources/icons/notation/guidatastore.png').resize((self.ICON_SIZE, self.ICON_SIZE)))
        # draw select background
        self.id.append(cnv.create_oval(x, y, x + self.WIDTH, y + self.HEIGHT, width=0))
        # draw icon
        self.id.append(cnv.create_image(x + self.WIDTH/2, y + self.HEIGHT/2, image=self.icon))
        # draw text
        self.draw_text(self.element.name, x + self.WIDTH/2, y + self.HEIGHT/2 - (self.ICON_SIZE/2) - self.TEXT_OFFSET)

    