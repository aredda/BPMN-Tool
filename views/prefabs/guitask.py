from tkinter import Canvas
from PIL import Image as img, ImageTk as imgTk
from helpers.cachemanager import CacheManager
from resources.colors import *
from views.prefabs.guiactivity import GUIActivity
from models.bpmn.task import Task, TaskType
from models.bpmndi.shape import BPMNShape
from models.bpmndi.bounds import Bounds

class GUITask(GUIActivity):

    def __init__(self, **args):
        GUIActivity.__init__(self, **args)

        self.element = args.get('element', Task())

    def draw_at(self, x, y):
        # draw the border
        GUIActivity.draw_at(self, x, y)
        # extract info
        tasktype = self.element.type
        # draw type icon
        if tasktype != TaskType.Default:    
            # attempt to retrieve from cache
            cachekey = 'img_' + str (self.element.type) + '_' + str(self.ICON_SIZE)
            iconpath = 'resources/icons/notation/' + str(tasktype).lower().split('.')[1] + '.png'
            self.type_icon = CacheManager.get_cached_image(cachekey)
            # cache image if not there
            if self.type_icon == None:
                self.type_icon = CacheManager.get_or_add_if_absent(cachekey, imgTk.PhotoImage(img.open(iconpath).resize((self.ICON_SIZE, self.ICON_SIZE))))
            cnv: Canvas = self.getcanvas()
            self.id.append(cnv.create_image(x + self.ICON_MARGIN, y + self.ICON_MARGIN, image=self.type_icon))
        # draw text
        self.draw_text(self.element.name, x + self.WIDTH/2, y + self.HEIGHT/2, self.WIDTH)

    def get_options(self):
        optlist = super().get_options()

        def corrector(t): return lambda e: self.configure(t)

        for t in list(TaskType):
            # skip current option
            if t == self.element.type: continue
            # proceed
            tstr = str(t).split('.')[1]
            optlist.append({
                'folder': 'resources/icons/notation/',
                'icon': (tstr.lower() if t != TaskType.Default else 'task') + '.png',
                'text': f'Change to {tstr} Task',
                'fg': gray2,
                'textfg': gray,
                'cmnd': corrector(t)
            })

        return optlist

    def configure(self, ttype):
        self.element.type = ttype
        self.erase()
        self.draw()