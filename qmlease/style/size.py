"""
format: <scope>_<field>_<level>
    scope:
        - comp (component)
        - bar
        - button
        - label
        - edit
        - card
        - ...
    field:
        - margin
        - padding
        - spacing
        - width
        - height
        - radius
    level:
        - xs
        - s
        - m
        - l
        - xl
examples:
    - margin_xs
    - margin_s
    - margin_m
    - margin_l
    - margin_xl
"""
from .base import Base
from .enum import pyenum


class Size(Base):
    _valid_sizes = ('xxs', 'xs', 's', 'm', 'l', 'xl', 'xxl')
    
    def __init__(self) -> None:
        super().__init__()
        for k, v in {
            'auto': pyenum.AUTO,
            'stretch': pyenum.STRETCH,
            'wrap': pyenum.WRAP,
        }.items():
            self.data[k] = v
            self.insert(k, v)
    
    def _normalize(self, data: dict) -> dict:
        new_data = {}
        for k, v in data.items():
            if '_' in k:
                a, b = k.rsplit('_', 1)
                if b in self._valid_sizes:
                    new_data[k] = v
                else:
                    new_data[f'{k}_m'] = v
            else:
                new_data[f'{k}_m'] = v
        return new_data
    
    def _create_similars(self, data: dict) -> dict:
        return {}
    
    def _shortify(self, data: dict) -> dict:
        new_data = {}
        for k, v in data.items():
            if k.endswith('_m'):
                new_data[k[:-2]] = v
        return new_data
