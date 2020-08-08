from tkinter import Canvas
from PIL import Image as Img, ImageTk as ImgTk
from helpers.cachemanager import CacheManager
from views.prefabs.abstract.prefab import Prefab
from models.bpmn.datastorereference import DataStoreReference
from models.bpmndi.shape import BPMNShape
from models.bpmndi.bounds import Bounds

class GUIDataStore(Prefab):

    ICON_SIZE = 50
    TEXT_OFFSET = 16

    def __init__(self, **args):
        super().__init__(**args)

        self.element = args.get('element', DataStoreReference())
        self.dielement = args.get('dielement', BPMNShape())

        if self.dielement.bounds == None:
            self.dielement.bounds = Bounds()

        self.WIDTH = self.HEIGHT = self.ICON_SIZE

    def draw_at(self, x, y):
        super().draw_at(x, y)

        self.icon = CacheManager.get_cached_image('img_dtstore') 
        if self.icon == None:
            self.icon = CacheManager.get_or_add_if_absent ('img_dtstore', ImgTk.PhotoImage(Img.open('resources/icons/notation/guidatastore.png').resize((self.ICON_SIZE, self.ICON_SIZE))))
        # draw select background
        self.id.append(self.canvas.create_oval(x, y, x + self.WIDTH, y + self.HEIGHT, width=0))
        # draw icon
        self.id.append(self.canvas.create_image(x + self.WIDTH/2, y + self.HEIGHT/2, image=self.icon))
        # draw text
        self.draw_text(self.element.name, x + self.WIDTH/2, y + self.HEIGHT/2 - (self.ICON_SIZE/2) - self.TEXT_OFFSET)

    def memento_setup(self):
        super().memento_setup()
        # turn off images
        self.icon = None