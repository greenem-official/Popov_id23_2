from enum import Enum


def load_style(file_path):
    with open(file_path, 'r') as file:
        return file.read()


class StyleType(Enum):
    NormalButton = 1,
    SectionTitle = 2,
    SimpleText = 3,

def getStyle(style):
    return styles[style]

styles = {}

def init():
    pass
    styles[StyleType.NormalButton] = load_style('data/styles/NormalButton.css')
    styles[StyleType.SectionTitle] = load_style('data/styles/SectionTitle.css')
    styles[StyleType.SimpleText] = load_style('data/styles/SimpleText.css')
