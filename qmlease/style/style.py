from lk_utils import xpath
from qtpy.QtQml import QQmlPropertyMap

from .color3 import Color
from .font import Font
from .motion import Motion
from .size import Size


class _Style(QQmlPropertyMap):
    color = Color()
    font = Font()
    motion = Motion()
    size = Size()
    
    def __init__(self) -> None:
        super().__init__(None)
        dir_ = xpath('./stylesheet')
        # self.color.update_from_file(f'{dir_}/color.yaml')
        self.font.update_from_file(f'{dir_}/font.yaml')
        self.motion.update_from_file(f'{dir_}/motion.yaml')
        self.size.update_from_file(f'{dir_}/size.yaml')
        self.insert('color', self.color)
        self.insert('font', self.font)
        self.insert('motion', self.motion)
        self.insert('size', self.size)


pystyle = _Style()
