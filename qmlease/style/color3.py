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
    ColorHex = str  # `#rrggbb`
    ColorKey = str
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
    _hex_to_token: tp.Dict[T.ColorHex, ColorToken]
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
        self._hex_to_token = {t.hex: t for t in self._color_palette.values()}
        self._is_dark_theme = False

    @Slot(str, result=str)
    @Slot(str, int, result=str)
    def higher(self, base: T.ColorHex, level: int = 1) -> T.ColorHex:
        tok = self._hex_to_token[base]
        return tok.higher(level).hex

    @Slot(str, result=str)
    @Slot(str, int, result=str)
    def lower(self, base: T.ColorHex, level: int = 1) -> T.ColorHex:
        tok = self._hex_to_token[base]
        return tok.lower(level).hex

    @Slot(str, result=str)
    @Slot(str, int, result=str)
    def lighter(self, base: T.ColorHex, level: int = 1) -> T.ColorHex:
        tok = self._hex_to_token[base]
        return tok.lighter(level).hex

    @Slot(str, result=str)
    @Slot(str, int, result=str)
    def darker(self, base: T.ColorHex, level: int = 1) -> T.ColorHex:
        tok = self._hex_to_token[base]
        return tok.darker(level).hex

    @Slot(str, result=str)
    def against(self, source: T.ColorHex) -> T.ColorHex:
        tok = self._hex_to_token[source]
        return ColorToken(
            (
                tok.h,
                tok.c,
                min((tok.t - 50, 20))
                if tok.is_light
                else max((tok.t + 50, 80)),
            )
        ).hex

    def _qget_color(self, key: T.ColorKey) -> T.ColorHex:
        return self._color_palette[key].hex
