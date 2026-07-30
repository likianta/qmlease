"""
inspiration:
    - https://github.com/T-Dynamos/materialyoucolor-python
    - https://github.com/sudoevolve/material-components-pyside
"""

import typing as tp
from collections import defaultdict
from functools import partial

import colorsys
from materialyoucolor.contrast import Contrast
from materialyoucolor.dynamiccolor.material_dynamic_colors import \
    MaterialDynamicColors
from materialyoucolor.hct import Hct
from materialyoucolor.scheme import SchemeFidelity
# from materialyoucolor.scheme import SchemeTonalSpot
# from qtpy.QtCore import Property
from qtpy.QtCore import Property as QtProperty

from ..qtcore import QObject
from ..qtcore import Signal
from ..qtcore import Slot
from ..qtcore import StaticProperty

_dynamic_color_system = MaterialDynamicColors(spec='2025')
# color_spec = MaterialDynamicColors(spec='2025').color_spec

class T:
    CustomRoles = tp.Tuple[tp.Tuple[str, str], ...]
    PresetRoles = tp.Tuple[str, ...]

class Color(QObject):
    black = StaticProperty('black')
    blue = StaticProperty('blue')
    # dark_theme = Property(False)
    green = StaticProperty('green')
    grey = StaticProperty('grey')
    magenta = StaticProperty('magenta')
    orange = StaticProperty('orange')
    pink = StaticProperty('pink')
    red = StaticProperty('red')
    transparent = StaticProperty('transparent')
    white = StaticProperty('white')
    yellow = StaticProperty('yellow')
    
    theme_changed = Signal(light_or_dark=bool)
    
    _cached_colors: tp.Dict[str, tp.Dict[str, 'ColorToken']]
    _current_scheme: tp.Dict[str, str]
    _custom_colors = {
        'light': {
            # 'surface': '#f9f9ff',  # titan white
            # 'primary': '#0969da',  # science blue
            # 'success': '#008000',  # japanese laurel
            # 'warning': '#fff25a',  # gorse
            'theme_blue': '#0969da',
            'theme_green': '#008000',
            'theme_yellow': '#fff25a',
        },
        'dark' : {
            # 'surface': '#10131a',  # bunker
            'theme_green': '#2ed563',  # shamrock
        }
    }
    _dark_scheme: tp.Dict[str, str]
    _is_dark_theme: bool
    _light_scheme: tp.Dict[str, str]
    _preset_roles: T.PresetRoles = (
        'primary',
        'on_primary',
        'primary_container',
        'on_primary_container',
        'secondary',
        'on_secondary',
        'secondary_container',
        'on_secondary_container',
        'tertiary',
        'on_tertiary',
        'tertiary_container',
        'on_tertiary_container',
        'error',
        'on_error',
        'error_container',
        'on_error_container',
        'background',
        'on_background',
        'surface',
        'on_surface',
        'surface_variant',
        'on_surface_variant',
        'outline',
        'outline_variant',
        'shadow',
        'scrim',
        'inverse_surface',
        'inverse_on_surface',
        'inverse_primary',
        'surface_dim',
        'surface_bright',
        'surface_container_lowest',
        'surface_container_low',
        'surface_container',
        'surface_container_high',
        'surface_container_highest',
    )
    _seed_color: str
    
    @staticmethod
    def __qinit__(attrs: dict):
        # dynamically register property names
        role_names = set()
        role_names.update(attrs['_preset_roles'])
        for name in {
            *attrs['_custom_colors']['light'].keys(),
            *attrs['_custom_colors']['dark'].keys()
        }:
            role_names.add(name)
            role_names.add('on_' + name)
            role_names.add(name + '_container')
            # role_names.add(name + '_outline')
            # role_names.add(name + '_outline_variant')
        for name in role_names:
            attrs[name] = QtProperty(
                str,
                fget=partial(attrs['_qget_color'], name=name),
                notify=attrs['theme_changed']
            )

    def __init__(self):
        super().__init__()
        
        # self._seed_color = '#6750A4'  # butterfly bush (md3 demo)
        # self._seed_color = '#214E80'  # bay of many
        self._seed_color = '#0969DA'  # science blue (primer css)
        
        argb = hex_to_argb(self._seed_color)
        self._light_scheme = self._generate_scheme(argb, is_dark=False)
        self._dark_scheme = self._generate_scheme(argb, is_dark=True)
        self._current_scheme = self._light_scheme
        self._cached_colors = defaultdict(dict)
        self._is_dark_theme = False

        # add custom colors to light/dark schemes
        if self._custom_colors['light'] or self._custom_colors['dark']:
            custom_dict_lt = self._custom_colors['light']
            custom_dict_dk = self._custom_colors['dark']
            
            surface_lt = hex_to_token(self._light_scheme['surface'])
            surface_dk = hex_to_token(self._dark_scheme['surface'])
            
            # mutual fill custom dict
            for name, hex in custom_dict_lt.items():
                if name not in custom_dict_dk.items():
                    color_lt = hex_to_token(hex)
                    color_dk = ColorToken((
                        color_lt.h,
                        color_lt.c,
                        surface_dk.t + (surface_lt.t - color_lt.t)
                    ))
                    assert color_dk.hex != color_lt.hex
                    custom_dict_dk[name] = color_dk.hex
            for name, hex in custom_dict_dk.items():
                if name not in custom_dict_lt.items():
                    color_dk = hex_to_token(hex)
                    color_lt = ColorToken((
                        color_dk.h,
                        color_dk.c,
                        surface_lt.t - (color_dk.t - surface_dk.t)
                    ))
                    assert color_lt.hex != color_dk.hex
                    custom_dict_lt[name] = color_lt.hex
            
            surface_container_lt = hex_to_token(
                self._light_scheme['surface_container']
            )
            surface_container_dk = hex_to_token(
                self._dark_scheme['surface_container']
            )
            for name, hex in custom_dict_lt.items():
                color = hex_to_token(hex)
                self._light_scheme.update({
                    name: hex,
                    'on_' + name: color.shift(12).hex,
                    name + '_container': ColorToken((
                        color.h,
                        color.c,
                        surface_container_lt.t
                    )).hex
                })
            for name, hex in custom_dict_dk.items():
                color = hex_to_token(hex)
                self._dark_scheme.update({
                    name: hex,
                    'on_' + name: color.shift(12).hex,
                    name + '_container': ColorToken((
                        color.h,
                        color.c,
                        surface_container_dk.t
                    )).hex
                })

    def _generate_scheme(self, argb: int, is_dark: bool) -> tp.Dict[str, str]:
        """
        returns: a dict of color hex strings. 
            e.g. {'primary': '#214E80', 'on_primary': '#FFFFFF', ...}
        """
        source = Hct.from_int(argb)
        # scheme = SchemeTonalSpot(source, is_dark, 0.0, spec_version='2025')
        scheme = SchemeFidelity(source, is_dark, 0.0, spec_version='2025')
        colors = _dynamic_color_system

        # tokens: 
        #   https://m3.material.io/styles/color/roles
        #   https://m3.material.io/foundations/design-tokens/overview
        out = {}
        for name in self._preset_roles:
            parts = name.split('_')
            token = parts[0] + ''.join(x.capitalize() for x in parts[1:])
            dyn = getattr(colors, token)
            hex = dyn.get_hex(scheme)  # e.g. '#6750A4FF'
            out[name] = hex[:-2]
        return out
    
    def _qget_color(self, name):
        # if name.startswith('theme_'):
        #     print(name, self._current_scheme[name], self._is_dark_theme, ':v')
        return self._current_scheme[name]
    
    # --------------------------------------------------------------------------

    @Slot(str, result=str)
    @Slot(str, str, result=str)
    @Slot(str, str, str, result=str)
    def get(
        self, value: str, variant: str = '', against: str = ''
    ) -> str:
        if not variant:
            return value

        if variant and variant in self._cached_colors[value]:
            return self._cached_colors[value][variant].hex

        def resolve_variant() -> ColorToken:
            # nonlocal variant
            color = hex_to_token(value)
            
            if variant == 'border':
                if against:  # FIXME
                    # -- a
                    # other = hex_to_token(against)
                    # ratio = 2.5
                    # out = color.shift(ratio)
                    # while out / other < 2:
                    #     ratio += 0.2
                    #     if ratio <= 21:
                    #         out = color.shift(ratio)
                    #     else:
                    #         ratio = 1.8
                    #         out = color.rshift(ratio)
                    #         while out / other < 2:
                    #             ratio += 0.2
                    #             if ratio <= 21:
                    #                 out = color.rshift(ratio)
                    #             else:
                    #                 raise Exception
                    #         return out
                    # return out
                    # -- b
                    a = color.shift(2.5)
                    b = hex_to_token(against)
                    if a / b >= 2:
                        return a
                    else:
                        c = b.shift(4.5)
                        return ColorToken((c.h, c.c, a.t))
                else:
                    return color.shift(2.5)
            
            elif variant == 'container':
                color0 = hex_to_token(self._current_scheme['surface'])
                color1 = hex_to_token(value)
                return ColorToken((color1.h, color1.c, color0.shift(0.2).t))
            
            elif variant == 'darker':
                color = hex_to_token(value)
                return color.darker()
            
            elif variant == 'lighter':
                color = hex_to_token(value)
                return color.lighter()
            
            elif variant == 'on':
                color = hex_to_token(value)
                return color.shift(12)
            
            elif variant == 'rshift':
                color = hex_to_token(value)
                return color.rshift(0.2)
            
            elif variant == 'shift':
                color = hex_to_token(value)
                return color.shift(0.2)
            
            elif variant == 'strong_border':
                return color.shift(4.5)
            
            elif variant == 'variant':
                color = hex_to_token(value)
                return color.shift(0.2)
            
            else:
                # if variant == 'on':
                #     variant = 'on_primary_container'
                scheme = SchemeFidelity(
                    Hct.from_int(hex_to_argb(value)), 
                    is_dark=self._is_dark_theme, 
                    contrast_level=0.0, 
                    spec_version='2025'
                )
                return ColorToken(
                    getattr(
                        _dynamic_color_system, _snake_to_camel_case(variant)
                    ).get_hex(scheme)[:-2]
                )
            # raise Exception(value, variant)

        out = self._cached_colors[value][variant] = resolve_variant()
        # print('{} & {} -> {} ({})'.format(
        #     value, variant, out.hex, 'dark' if self._is_dark_theme else 'light'
        # ), ':v')
        return out.hex

    @Slot(str, str, str, result=str)
    def derive(self, ref0, ref1, to0) -> str:
        # https://chatgpt.com/share/69c20008-a9c8-800a-ba49-b36cca026a0b
        def hex_to_rgb(value: str) -> tp.Tuple[int, int, int]:
            return (
                int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16)
            )

        def rgb_to_hls(r: int, g: int, b: int) -> tp.Tuple[float, float, float]:
            return colorsys.rgb_to_hls(r / 255, g / 255, b / 255)

        def hls_to_hex(h: float, l: float, s: float) -> str:
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'
        
        def adjust_lightness(hex_color, factor):
            """
            params:
                factor: >1 will be lighter, <1 will be darker.
            """
            r, g, b = hex_to_rgb(hex_color)
            h, l, s = rgb_to_hls(r, g, b)
            return hls_to_hex(h, l * factor, s)

        ref1_hls = rgb_to_hls(*hex_to_rgb(ref1))
        ref0_hls = rgb_to_hls(*hex_to_rgb(ref0))
        factor = ref1_hls[1] / ref0_hls[1]
        # print(factor, ':v')
        return adjust_lightness(to0, factor)

    @Slot(str, str, str, result=str)
    def derive2(self, ref0, ref1, val0):
        hct0 = hex_to_hct(ref0)
        hct1 = hex_to_hct(ref1)
        hct2 = hex_to_hct(val0)
        hct3 = Hct.from_hct(
            hct2.hue, hct2.chroma, hct2.tone + (hct1.tone - hct0.tone)
        )
        return hct_to_hex(hct3)

    # --------------------------------------------------------------------------
    
    def _qget_dark_theme(self):
        return self._is_dark_theme

    def _qset_dark_theme(self, is_dark: bool):
        if self._is_dark_theme == is_dark:
            return
        self._is_dark_theme = is_dark
        self._current_scheme = (
            self._dark_scheme if is_dark else self._light_scheme
        )
        self._cached_colors.clear()
        self.theme_changed.emit(not self._is_dark_theme)

    dark_theme = QtProperty(bool, _qget_dark_theme, _qset_dark_theme)  # noqa

class ColorToken:
    
    def __init__(
        self, value: tp.Union[str, Hct, tp.Tuple[float, float, float]]
    ) -> None:
        if isinstance(value, str):
            self.hex = value
            self.int = int(value[1:], 16)
            hct = hex_to_hct(value)
            self.hue = hct.hue
            self.chroma = hct.chroma
            self.tone = hct.tone
        else:
            hct = value if isinstance(value, Hct) else Hct.from_hct(*value)
            self.hex = hct_to_hex(hct)
            self.int = hct.to_int() & 0xFFFFFF
            self.hue = hct.hue
            self.chroma = hct.chroma
            self.tone = hct.tone

    def __hash__(self) -> int:
        return self.int

    def __str__(self) -> str:
        return '<ColorToken {} (h={:.0f}, c={:.0f}, t={:.0f})'.format(
            self.hex, self.hue, self.chroma, self.tone
        )
    
    def __truediv__(self, other: 'ColorToken') -> float:
        return Contrast.ratio_of_tones(self.tone, other.tone)

    @property
    def h(self) -> float:
        return self.hue
    
    @property
    def c(self) -> float:
        return self.chroma
    
    @property
    def t(self) -> float:
        return self.tone

    @property
    def hct(self):
        return self.hue, self.chroma, self.tone
    
    def dark_against(self, ratio: float = 4.5):
        return ColorToken(
            (self.h, self.c, Contrast.darker_unsafe(self.tone, ratio))
        )
    
    def darker(self, ratio: float = 0.2):
        return ColorToken(
            (self.h, self.c, Contrast.darker_unsafe(self.tone, 1 + ratio))
        )
    
    def light_against(self, ratio: float = 4.5):
        return ColorToken(
            (self.h, self.c, Contrast.lighter_unsafe(self.tone, ratio))
        )
    
    def lighter(self, ratio: float = 0.2):
        return ColorToken(
            (self.h, self.c, Contrast.lighter_unsafe(self.tone, 1 + ratio))
        )
    
    def shift(self, ratio: float = 0.2):
        if ratio <= 1:
            return (
                self.lighter(ratio) if self.tone < 50 else self.darker(ratio)
            )
        else:
            return (
                self.light_against(ratio) if self.tone < 50 else
                self.dark_against(ratio)
            )
    
    def rshift(self, ratio: float = 0.2):
        if ratio <= 1:
            return (
                self.lighter(ratio) if self.tone >= 50 else self.darker(ratio)
            )
        else:
            return (
                self.light_against(ratio) if self.tone >= 50 else
                self.dark_against(ratio)
            )
    
    # def shift_against(self, ratio: float = 4.5):
    #     return (
    #         self.light_against(ratio) if self.tone < 50 else
    #         self.dark_against(ratio)
    #     )

# ------------------------------------------------------------------------------

def argb_to_hex(argb: int) -> str:
    return f'#{argb & 0xFFFFFF:06x}'

def auto_shift(value, ratio):
    hct = hex_to_hct(value)
    return hct_to_hex(
        Hct.from_hct(
            hct.hue, 
            hct.chroma, 
            (
                Contrast.darker_unsafe if hct.tone > 50 else 
                Contrast.lighter_unsafe
            )(hct.tone, ratio if ratio > 1 else 1 + ratio)
        )
    )

def darker(value, ratio):
    if ratio > 1:
        return _abs_darker(value, ratio)
    else:
        return _rel_darker(value, ratio)

def hct_to_hex(hct: Hct) -> str:
    return argb_to_hex(hct.to_int())

def hex_to_argb(value: str) -> int:
    # assert value[0] == '#' and len(value) == 7
    # return (int(value[1:], 16) << 8) | 0xFF
    return 0xFF << 24 | int(value.removeprefix('#'), 16)

def hex_to_hct(value: str) -> Hct:
    argb = hex_to_argb(value)
    return Hct.from_int(argb)

def hex_to_token(value: str) -> ColorToken:
    return ColorToken(value)

def lighter(value, ratio):
    if ratio > 1:
        return _abs_lighter(value, ratio)
    else:
        return _rel_lighter(value, ratio)

def _abs_darker(value, ratio: float = 5):
    """
    ratio:
        ref: https://chatgpt.com/share/69c3adf2-02f0-83a9-8a0d-46b3a7bc2d73
        minimum: 1.0 -> no change (same color).
        maximum: 21.0 -> max contrast (pure black vs pure white).
        the higher the ratio, the darker the color.
    """
    hct = hex_to_hct(value)
    return hct_to_hex(
        Hct.from_hct(
            hct.hue, 
            hct.chroma, 
            Contrast.darker_unsafe(hct.tone, ratio)
        )
    )

def _abs_lighter(value, ratio: float = 5):
    hct = hex_to_hct(value)
    return hct_to_hex(
        Hct.from_hct(
            hct.hue, 
            hct.chroma, 
            Contrast.lighter_unsafe(hct.tone, ratio)
        )
    )

def _camel_to_snake_case(name: str) -> str:
    return ''.join(('_' + i.lower() if i.isupper() else i for i in name))

def _rel_darker(value, ratio: float = 0.2):
    """
    darken color relative to its ratio.
    ratio: 0.0 ~ 1.0. for example, 0.2 -> 20% darker.
    """
    hct = hex_to_hct(value)
    return hct_to_hex(
        Hct.from_hct(
            hct.hue, 
            hct.chroma, 
            Contrast.darker_unsafe(hct.tone, 1 + ratio)
        )
    )

def _rel_lighter(value, ratio: float = 0.2):
    hct = hex_to_hct(value)
    return hct_to_hex(
        Hct.from_hct(
            hct.hue, 
            hct.chroma, 
            Contrast.lighter_unsafe(hct.tone, 1 + ratio)
        )
    )

def _snake_to_camel_case(name: str) -> str:
    parts = name.split('_')
    return parts[0] + ''.join(x.capitalize() for x in parts[1:])
