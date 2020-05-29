from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from os.path import *

def svg_to_png(svgFilePath, pngOutputPath):
    drawn = svg2rlg(svgFilePath)
    renderPM.drawToFile(drawn, pngOutputPath, fmt='PNG')

    return pngOutputPath

def svg_has_temp(svgFilePath):
    pass