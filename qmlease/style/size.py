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
from .base import T
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
    
    def _normalize(self, data: T.Data) -> T.Data:
        for k, v in data:
            if k.endswith('_m'):
                yield k, v
                yield k[:-2], v
            elif '_' in k:
                a, b = k.rsplit('_', 1)
                if b in self._valid_sizes:
                    yield k, v
                else:
                    yield f'{k}_m', v
            else:
                yield f'{k}_m', v
    
    def _create_similars(self, data: T.Data) -> T.Data:
        return data
    
    def _shortify(self, data: T.Data) -> T.Data:
        for k, v in data:
            if k.endswith('_m'):
                yield k[:-2], v
