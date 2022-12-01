from qtpy.QtCore import Property
from qtpy.QtCore import QObject

from .color import Color
from .font import Font
from .motion import Motion
from .size import Size


class Style:
    color = Color()
    font = Font()
    motion = Motion()
    size = Size()
    
    def __init__(self):
        from lk_utils import relpath
        assets_dir = relpath('./stylesheet')
        self.color.update_from_file(f'{assets_dir}/color.yaml')
        self.font.update_from_file(f'{assets_dir}/font.yaml')
        self.motion.update_from_file(f'{assets_dir}/motion.yaml')
        self.size.update_from_file(f'{assets_dir}/size.yaml')


class StyleForQml(QObject):
    # `Property : param constant`: https://stackoverflow.com/questions/6728615
    #   /warning-about-non-notifyable-properties-in-qml
    color = Property(Color, lambda _: Style.color, constant=True)
    font = Property(Font, lambda _: Style.font, constant=True)
    motion = Property(Motion, lambda _: Style.motion, constant=True)
    size = Property(Size, lambda _: Style.size, constant=True)


pystyle = Style()
pystyle_for_qml = StyleForQml(None)
