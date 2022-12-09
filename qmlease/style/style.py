from lk_utils import xpath
from qtpy.QtQml import QQmlPropertyMap

from .color import Color
from .font import Font
from .motion import Motion
from .size import Size


class Style(QQmlPropertyMap):
    color = Color()
    font = Font()
    motion = Motion()
    size = Size()
    
    def __init__(self):
        super().__init__(None)
        dir_ = xpath('./stylesheet')
        self.color.update_from_file(f'{dir_}/color.yaml')
        self.font.update_from_file(f'{dir_}/font.yaml')
        self.motion.update_from_file(f'{dir_}/motion.yaml')
        self.size.update_from_file(f'{dir_}/size.yaml')
        self.insert('color', self.color)
        self.insert('font', self.font)
        self.insert('motion', self.motion)
        self.insert('size', self.size)


# class StyleForQml(QObject):
#     # `Property : param constant`: https://stackoverflow.com/questions/6728615
#     #   /warning-about-non-notifyable-properties-in-qml
#     color = Property(Color, lambda _: Style.color, constant=True)
#     font = Property(Font, lambda _: Style.font, constant=True)
#     motion = Property(Motion, lambda _: Style.motion, constant=True)
#     size = Property(Size, lambda _: Style.size, constant=True)


pystyle = Style()
