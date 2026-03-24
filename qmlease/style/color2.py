"""
inspiration:
    - https://github.com/T-Dynamos/materialyoucolor-python
    - https://github.com/sudoevolve/material-components-pyside
"""
import colorsys
import typing as t
from collections import defaultdict
from functools import partial
from materialyoucolor.contrast import Contrast
from materialyoucolor.dynamiccolor.material_dynamic_colors import \
    MaterialDynamicColors
from materialyoucolor.hct import Hct
from materialyoucolor.scheme import SchemeFidelity
# from materialyoucolor.scheme import SchemeTonalSpot
# from qtpy.QtCore import Property
from qtpy.QtCore import Property as QtProperty
from qtpy.QtGui import QColor
from ..qtcore import QObject
from ..qtcore import Signal
from ..qtcore import Slot
from ..qtcore import StaticProperty

_dynamic_color_system = MaterialDynamicColors(spec='2025')
# color_spec = MaterialDynamicColors(spec='2025').color_spec

class T:
    CustomRoles = t.Tuple[t.Tuple[str, str], ...]
    PresetRoles = t.Tuple[str, ...]

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
    
    _cached_hex_colors: t.Dict[str, t.Dict[str, str]]
    _current_scheme: t.Dict[str, str]
    _custom_colors_for_dark_theme: T.CustomRoles = (
        # ('success', '#2ed563'),
    )
    _custom_colors_for_light_theme: T.CustomRoles = (
        # you can override the custom colors in subclass.
        ('theme_blue', '#0969da'),
        ('theme_green', '#008000'),
        ('theme_yellow', '#fff25a'),
    )
    _dark_scheme: t.Dict[str, str]
    _is_dark_theme: bool
    _light_scheme: t.Dict[str, str]
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
        for name, _ in (
            attrs['_custom_colors_for_light_theme'] +
            attrs['_custom_colors_for_dark_theme']
        ):
            role_names.add(name)
            role_names.add('on_' + name)
            role_names.add(name + '_container')
            role_names.add(name + '_outline')
            role_names.add(name + '_outline_variant')
        
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
        self._cached_hex_colors = defaultdict(dict)
        self._is_dark_theme = False

        # add custom colors to light/dark schemes
        if (
            self._custom_colors_for_light_theme or
            self._custom_colors_for_dark_theme
        ):
            custom_dict_0 = dict(self._custom_colors_for_light_theme)
            custom_dict_1 = dict(self._custom_colors_for_dark_theme)
            p0, p1, p2, p3, p4, p5 = (
                getattr(_dynamic_color_system, 'primary'),
                getattr(_dynamic_color_system, 'onPrimary'),
                getattr(_dynamic_color_system, 'primaryContainer'),
                getattr(_dynamic_color_system, 'onPrimaryContainer'),
                getattr(_dynamic_color_system, 'outline'),
                getattr(_dynamic_color_system, 'outlineVariant'),
            )
            
            for name, hex_ in custom_dict_0.items():
                source = Hct.from_int(hex_to_argb(hex_))
                scheme = SchemeFidelity(
                    source, is_dark=False, contrast_level=0.0
                )
                self._light_scheme.update({
                    name: p2.get_hex(scheme)[:-2],
                    'on_' + name: p3.get_hex(scheme)[:-2],
                    name + '_container': p0.get_hex(scheme)[:-2],
                    name + '_outline': p4.get_hex(scheme)[:-2],
                    name + '_outline_variant': p5.get_hex(scheme)[:-2],
                })
                if name not in custom_dict_1:
                    scheme = SchemeFidelity(
                        source, is_dark=True, contrast_level=0.0
                    )
                    self._dark_scheme.update({
                        name: p2.get_hex(scheme)[:-2],
                        'on_' + name: p3.get_hex(scheme)[:-2],
                        name + '_container': p1.get_hex(scheme)[:-2],
                        name + '_outline': p4.get_hex(scheme)[:-2],
                        name + '_outline_variant': p5.get_hex(scheme)[:-2],
                    })
            
            for name, hex_ in custom_dict_1.items():
                source = Hct.from_int(hex_to_argb(hex_))
                scheme = SchemeFidelity(
                    source, is_dark=True, contrast_level=0.0
                )
                self._dark_scheme.update({
                    name: p2.get_hex(scheme)[:-2],
                    'on_' + name: p3.get_hex(scheme)[:-2],
                    name + '_container': p1.get_hex(scheme)[:-2],
                    name + '_outline': p4.get_hex(scheme)[:-2],
                    name + '_outline_variant': p5.get_hex(scheme)[:-2],
                })
                if name not in custom_dict_0:
                    scheme = SchemeFidelity(
                        source, is_dark=False, contrast_level=0.0
                    )
                    self._light_scheme.update({
                        name: p0.get_hex(scheme)[:-2],
                        'on_' + name: p1.get_hex(scheme)[:-2],
                        name + '_container': p0.get_hex(scheme)[:-2],
                        name + '_outline': p4.get_hex(scheme)[:-2],
                        name + '_outline_variant': p5.get_hex(scheme)[:-2],
                    })

        # for name in self._current_scheme:
        #     if name.startswith('on_') or '_outline' in name:
        #         continue
        #     if name.endswith('_container'):
        #         self._cached_hex_colors[self._current_scheme[name]] = {
        #             'on': (
        #                 self._current_scheme['on_' + name] 
        #                 if 'on_' + name in self._current_scheme else 
        #                 self._current_scheme[
        #                     'on_' + name.removesuffix('_container')
        #                 ]
        #             )
        #         }
        #     else:
        #         if (
        #             'on_' + name in self._current_scheme and 
        #             name + '_container' in self._current_scheme
        #         ):
        #             self._cached_hex_colors[self._current_scheme[name]] = {
        #                 'on': 
        #                     self._current_scheme['on_' + name],
        #                 'container': 
        #                     self._current_scheme[name + '_container'],
        #                 'outline': 
        #                     self._current_scheme.get(name + '_outline', ''),
        #                 'outline_variant': 
        #                     self._current_scheme.get(
        #                         name + '_outline_variant', ''
        #                     ),
        #             }

    def _generate_scheme(self, argb: int, is_dark: bool) -> t.Dict[str, str]:
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
        return self._current_scheme[name]
    
    # --------------------------------------------------------------------------

    @Slot(str, result=str)
    @Slot(str, str, result=str)
    def get(self, value: str, variant: str = '') -> str:
        if not variant:
            return value

        if variant and variant in self._cached_hex_colors[value]:
            return self._cached_hex_colors[value][variant]

        def resolve_variant():
            nonlocal variant
            if variant == 'border':
                hct0 = hex_to_hct(self._current_scheme['surface'])
                hct1 = hex_to_hct(value)
                return hct_to_hex(
                    Hct.from_hct(
                        hct1.hue, 
                        hct1.chroma, 
                        hct1.tone 
                        if Contrast.ratio_of_tones(hct0.tone, hct1.tone) >= 4.5 
                        else Contrast.darker_unsafe(hct0.tone, 4.5)
                    )
                )
            elif variant == 'container':
                hct0 = hex_to_hct(
                    self._current_scheme['surface_container_highest']
                )
                hct1 = hex_to_hct(value)
                return hct_to_hex(
                    Hct.from_hct(hct1.hue, hct1.chroma, hct0.tone)
                )
            elif variant == 'darker':
                return darker(value)
            elif variant == 'lighter':
                return lighter(value)
            elif variant == 'on':
                return darker(value, 12)
            elif variant == 'variant':
                return darker(value)
            else:
                # if variant == 'on':
                #     variant = 'on_primary_container'
                scheme = SchemeFidelity(
                    Hct.from_int(hex_to_argb(value)), 
                    is_dark=self._is_dark_theme, 
                    contrast_level=0.0, 
                    spec_version='2025'
                )
                return getattr(
                    _dynamic_color_system, _snake_to_camel_case(variant)
                ).get_hex(scheme)[:-2]
            # raise Exception(value, variant)

        out = self._cached_hex_colors[value][variant] = resolve_variant()
        # print('{} & {} -> {} ({})'.format(
        #     value, variant, out, 'dark' if self._is_dark_theme else 'light'
        # ), ':v')
        return out

    @Slot(str, result=str)
    def on(self, color_hex: str) -> str:
        if color_hex in self._cached_hex_colors:
            return self._cached_hex_colors[color_hex]['on']
        # https://chatgpt.com/s/t_69c237dd1ea08191ad77a4481fe07346
        bg = Hct.from_int(hex_to_argb(color_hex))
        fg_light = Hct.from_hct(bg.hue, bg.chroma, 100)
        fg_dark = Hct.from_hct(bg.hue, bg.chroma, 0)
        fg_light_ratio = Contrast.ratio_of_tones(fg_light.tone, bg.tone)
        fg_dark_ratio = Contrast.ratio_of_tones(fg_dark.tone, bg.tone)
        min_ratio = 4.5
        if fg_light_ratio >= min_ratio or fg_light_ratio >= fg_dark_ratio:
            out = argb_to_hex(fg_light.to_int())
        else:
            out = argb_to_hex(fg_dark.to_int())
        self._cached_hex_colors[color_hex]['on'] = out
        return out

    @Slot(str, str, str, result=str)
    def derive(self, ref0, ref1, to0) -> str:
        # https://chatgpt.com/share/69c20008-a9c8-800a-ba49-b36cca026a0b
        def hex_to_rgb(value: str) -> t.Tuple[int, int, int]:
            return (
                int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16)
            )

        def rgb_to_hls(r: int, g: int, b: int) -> t.Tuple[float, float, float]:
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
        self._cached_hex_colors.clear()
        self.theme_changed.emit(not self._is_dark_theme)

    dark_theme = QtProperty(bool, _qget_dark_theme, _qset_dark_theme)  # noqa

def argb_to_hex(argb: int) -> str:
    return f'#{argb & 0xFFFFFF:06x}'

def darker(hex, ratio: float = 5):
    """
    ratio:
        ref: https://chatgpt.com/share/69c3adf2-02f0-83a9-8a0d-46b3a7bc2d73
        minimum: 1.0 -> no change (same color).
        maximum: 21.0 -> max contrast (pure black vs pure white).
        the higher the ratio, the darker the color.
    """
    hct = hex_to_hct(hex)
    return hct_to_hex(
        Hct.from_hct(
            hct.hue, 
            hct.chroma, 
            Contrast.darker_unsafe(hct.tone, ratio)
        )
    )

def hct_to_hex(hct: Hct) -> str:
    return argb_to_hex(hct.to_int())

def hex_to_argb(value: str) -> int:
    # assert value[0] == '#' and len(value) == 7
    # return (int(value[1:], 16) << 8) | 0xFF
    return 0xFF << 24 | int(value.removeprefix('#'), 16)

def hex_to_hct(value: str) -> Hct:
    argb = hex_to_argb(value)
    return Hct.from_int(argb)

def lighter(hex):
    hct1 = Hct.from_int(hex_to_argb(hex))
    hct0 = Hct.from_hct(hct1.hue, hct1.chroma, 90)
    hex0 = argb_to_hex(hct0.to_int())
    return hex0

def _camel_to_snake_case(name: str) -> str:
    return ''.join(('_' + i.lower() if i.isupper() else i for i in name))

def _snake_to_camel_case(name: str) -> str:
    parts = name.split('_')
    return parts[0] + ''.join(x.capitalize() for x in parts[1:])
