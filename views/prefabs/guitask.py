from tkinter import Canvas
from PIL import Image as img, ImageTk as imgTk
from resources.colors import *
from views.prefabs.guiactivity import GUIActivity
from models.bpmn.task import Task, TaskType
from models.bpmndi.shape import BPMNShape

class GUITask(GUIActivity):

    def __init__(self, **args):
        GUIActivity.__init__(self, **args)

        self.element = args.get('element', Task())
        self.dielement = args.get('dielement', BPMNShape())

    def draw_at(self, x, y):
        # draw the border
        GUIActivity.draw_at(self, x, y)
        # extract info
        tasktype = self.element.type
        # draw type icon
        if tasktype != TaskType.Default:    
            iconpath = 'resources/icons/notation/' + str(tasktype).lower().split('.')[1] + '.png'
            self.type_icon = imgTk.PhotoImage(img.open(iconpath).resize((self.ICON_SIZE, self.ICON_SIZE)))
            cnv: Canvas = self.canvas
            self.id.append(cnv.create_image(x + self.ICON_MARGIN, y + self.ICON_MARGIN, image=self.type_icon))
        # draw text
        self.draw_text(self.element.name, x + self.WIDTH/2, y + self.HEIGHT/2, self.WIDTH)

    def get_options(self):
        optlist = super().get_options()

        def corrector(t): return lambda e: self.configure(t)

        for t in list(TaskType):
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