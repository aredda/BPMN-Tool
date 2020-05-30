from io import BytesIO
from PIL import ImageTk, Image


def getdisplayableimage(imagedata: bytes, size: tuple):
    img = Image.open(BytesIO(imagedata))
    return ImageTk.PhotoImage(img.resize(size))
