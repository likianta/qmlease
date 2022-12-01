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
from ._base import Base
from ..qt_core import slot


class Size(Base):
    
    def _post_complete(self, data: dict) -> dict:
        for k, v in tuple(data.items()):
            if not k.endswith('_m'):
                data[f'{k}_m'] = v
        return data
    
    @slot(str, result=int)
    @slot(str, int, result=int)
    def get_size_of_text(self):
        pass
