"""
inspiration:
    - https://github.com/T-Dynamos/materialyoucolor-python
    - https://github.com/sudoevolve/material-components-pyside
"""

import typing as t
from functools import partial
from materialyoucolor.dynamiccolor.material_dynamic_colors import \
    MaterialDynamicColors
from materialyoucolor.hct import Hct
from materialyoucolor.scheme import SchemeFidelity
from materialyoucolor.scheme import SchemeTonalSpot
# from qtpy.QtCore import Property
from qtpy.QtCore import Property as QtProperty
from qtpy.QtGui import QColor
from ..qtcore import QObject
from ..qtcore import StaticProperty
from ..qtcore import Signal

_dynamic_color_system = MaterialDynamicColors(spec='2025')

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
    
    _current_scheme: t.Dict[str, str]
    _custom_colors_for_dark_theme: T.CustomRoles = (
        # ('success', '#2ED563'),
    )
    _custom_colors_for_light_theme: T.CustomRoles = (
        # you can override the custom colors in subclass.
        ('theme_blue', '#0969DA'),
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
            # role_names.add(name + '_container')
            # role_names.add('on_' + name + '_container')
        
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
        
        argb = _hex_to_argb(self._seed_color)
        self._light_scheme = self._generate_scheme(argb, is_dark=False)
        self._dark_scheme = self._generate_scheme(argb, is_dark=True)
        self._current_scheme = self._light_scheme
        self._is_dark_theme = False
        
        if (
            self._custom_colors_for_light_theme or
            self._custom_colors_for_dark_theme
        ):
            custom_dict_0 = dict(self._custom_colors_for_light_theme)
            custom_dict_1 = dict(self._custom_colors_for_dark_theme)
            p0, p1, p2, p3 = (
                getattr(_dynamic_color_system, 'primary'),
                getattr(_dynamic_color_system, 'onPrimary'),
                getattr(_dynamic_color_system, 'primaryContainer'),
                getattr(_dynamic_color_system, 'onPrimaryContainer'),
            )
            # primary = getattr(_dynamic_color_system, 'primaryContainer')
            # on_primary = getattr(_dynamic_color_system, 'onPrimaryContainer')
            
            for name, hex_ in custom_dict_0.items():
                source = Hct.from_int(_hex_to_argb(hex_))
                scheme = SchemeFidelity(
                    source, is_dark=False, contrast_level=0.0
                )
                # self._light_scheme.update({
                #     name: p0.get_hex(scheme)[:-2],
                #     'on_' + name: p1.get_hex(scheme)[:-2],
                #     name + '_container': p2.get_hex(scheme)[:-2],
                #     'on_' + name + '_container': p3.get_hex(scheme)[:-2],
                # })
                self._light_scheme.update({
                    name        : p2.get_hex(scheme)[:-2],
                    'on_' + name: p3.get_hex(scheme)[:-2],
                })
                if name not in custom_dict_1:
                    scheme = SchemeFidelity(
                        source, is_dark=True, contrast_level=0.0
                    )
                    # self._dark_scheme.update({
                    #     name: p0.get_hex(scheme)[:-2],
                    #     'on_' + name: p1.get_hex(scheme)[:-2],
                    #     name + '_container': p2.get_hex(scheme)[:-2],
                    #     'on_' + name + '_container': p3.get_hex(scheme)[:-2],
                    # })
                    self._dark_scheme.update({
                        name        : p2.get_hex(scheme)[:-2],
                        'on_' + name: p3.get_hex(scheme)[:-2],
                    })
            
            for name, hex_ in custom_dict_1.items():
                source = Hct.from_int(_hex_to_argb(hex_))
                scheme = SchemeFidelity(
                    source, is_dark=True, contrast_level=0.0
                )
                self._dark_scheme.update({
                    name        : p2.get_hex(scheme)[:-2],
                    'on_' + name: p3.get_hex(scheme)[:-2],
                })
                if name not in custom_dict_0:
                    scheme = SchemeFidelity(
                        source, is_dark=False, contrast_level=0.0
                    )
                    self._light_scheme.update({
                        name        : p0.get_hex(scheme)[:-2],
                        'on_' + name: p1.get_hex(scheme)[:-2],
                    })

    def _generate_scheme(self, argb: int, is_dark: bool) -> t.Dict[str, str]:
        """
        returns: a dict of color hex strings. 
            e.g. {'primary': '#214E80', 'on_primary': '#FFFFFF', ...}
        """
        source = Hct.from_int(argb)
        scheme = SchemeTonalSpot(source, is_dark, 0.0, spec_version='2025')
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
    
    def _qget_dark_theme(self):
        return self._is_dark_theme

    def _qset_dark_theme(self, is_dark: bool):
        if self._is_dark_theme == is_dark:
            return
        self._is_dark_theme = is_dark
        self._current_scheme = (
            self._dark_scheme if is_dark else self._light_scheme
        )
        self.theme_changed.emit(not self._is_dark_theme)

    dark_theme = QtProperty(bool, _qget_dark_theme, _qset_dark_theme)  # noqa

def _camel_to_snake_case(name: str) -> str:
    return ''.join(('_' + i.lower() if i.isupper() else i for i in name))

def _hex_to_argb(value: str) -> int:
    assert value[0] == '#' and len(value) == 7
    # return (int(value[1:], 16) << 8) | 0xFF
    return 0xFF << 24 | int(value[1:], 16)

def _qcolor_to_argb(color: QColor) -> int:
    return int(color.rgba()) & 0xFFFFFFFF
