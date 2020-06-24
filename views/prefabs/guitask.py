from tkinter import Canvas
from PIL import Image as img, ImageTk as imgTk
from resources.colors import *
from views.prefabs.guiactivity import GUIActivity
from models.bpmn.enums.tasktype import TaskType

class GUITask(GUIActivity):

    def __init__(self, **args):
        GUIActivity.__init__(self, **args)

    def draw_at(self, x, y):
        # draw the border
        GUIActivity.draw_at(self, x, y)
        # extract info
        tasktype = TaskType.Script
        # draw type icon
        if tasktype != TaskType.Default:    
            iconpath = 'resources/icons/notation/' + str(tasktype).lower().split('.')[1] + '.png'
            self.type_icon = imgTk.PhotoImage(img.open(iconpath).resize((self.ICON_SIZE, self.ICON_SIZE)))
            cnv: Canvas = self.canvas
            cnv.create_image(x + self.ICON_MARGIN, y + self.ICON_MARGIN, image=self.type_icon)
