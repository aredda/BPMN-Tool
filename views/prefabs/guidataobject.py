from tkinter import Canvas
from PIL import Image as Img, ImageTk as ImgTk
from helpers.cachemanager import CacheManager
from views.prefabs.abstract.prefab import Prefab
from models.bpmn.dataobject import DataObject
from models.bpmndi.shape import BPMNShape
from models.bpmndi.bounds import Bounds

class GUIDataObject(Prefab):

    ICON_SIZE = 30
    RATIO = 1.3
    TEXT_OFFSET = 20

    def __init__(self, **args):
        super().__init__(**args)

        self.element = args.get('element', DataObject())
        self.dielement = args.get('dielement', BPMNShape())

        if self.dielement.bounds == None:
            self.dielement.bounds = Bounds()

        self.WIDTH = self.HEIGHT = self.ICON_SIZE

    def draw_at(self, x, y):
        super().draw_at(x, y)

        self.icon = CacheManager.get_cached_image('img_dtobj')
        if self.icon == None:
            self.icon = CacheManager.get_or_add_if_absent('img_dtobj', ImgTk.PhotoImage(Img.open('resources/icons/notation/guidataobject.png').resize((self.ICON_SIZE, int (self.ICON_SIZE * self.RATIO)))))
        # draw select background
        self.id.append(self.canvas.create_oval(x, y, x + self.WIDTH, y + self.HEIGHT, width=0))
        # draw icon
        self.id.append(self.canvas.create_image(x + self.WIDTH/2, y + self.HEIGHT/2, image=self.icon))
        # draw text
        self.draw_text(self.element.name, x + self.WIDTH/2, y + self.HEIGHT/2 - (self.ICON_SIZE/2) - self.TEXT_OFFSET)

    def memento_setup(self):
        super().memento_setup()
        # disable images
        self.icon = None