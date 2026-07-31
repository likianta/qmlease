import typing as tp
from functools import partial

from qmlease_colorsys import ColorToken
from qmlease_colorsys import generate_color_palette
from qtpy.QtCore import Property as QtProperty

from ..qtcore import Property
from ..qtcore import QObject
from ..qtcore import Signal
from ..qtcore import Slot
from ..qtcore import StaticProperty


class T:
    ColorKey = str
    ColorHex = str  # `#rrggbb`
    ColorPalette = tp.Dict[ColorKey, ColorToken]
    ColorToken = ColorToken


class Color(QObject):
    black = StaticProperty('black')
    white = StaticProperty('white')
    transparent = StaticProperty('transparent')

    theme_light = Property('#f9f9ff')
    theme_dark = Property('#10131a')

    theme_changed = Signal(is_light=bool)

    _color_palette: T.ColorPalette
    _is_dark_theme: bool

    @staticmethod
    def __before_init__(attrs: dict) -> None:
        attrs['_color_palette'] = generate_color_palette(seed='#0969da')
        for k in attrs['_color_palette']:
            attrs[k] = QtProperty(
                str,
                fget=partial(attrs['_qget_color'], key=k),
                notify=attrs['theme_changed'],
            )

    def __init__(self) -> None:
        super().__init__()
        self._is_dark_theme = False

    @Slot(str, result=str)
    @Slot(str, int, result=str)
    def higher(self, base: T.ColorKey, level: int = 1) -> T.ColorHex:
        tok = self._color_palette[base]
        return tok.higher(level).hex

    @Slot(str, result=str)
    @Slot(str, int, result=str)
    def lower(self, base: T.ColorKey, level: int = 1) -> T.ColorHex:
        tok = self._color_palette[base]
        return tok.lower(level).hex

    @Slot(str, result=str)
    @Slot(str, int, result=str)
    def lighter(self, base: T.ColorKey, level: int = 1) -> T.ColorHex:
        tok = self._color_palette[base]
        return tok.lighter(level).hex

    @Slot(str, result=str)
    @Slot(str, int, result=str)
    def darker(self, base: T.ColorKey, level: int = 1) -> T.ColorHex:
        tok = self._color_palette[base]
        return tok.darker(level).hex

    def _qget_color(self, key: T.ColorKey) -> T.ColorHex:
        return self._color_palette[key].hex
