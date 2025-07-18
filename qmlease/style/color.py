"""
naming style:
    component_part_state
        component: button, text, panel, win, ...
        part: bg, border, text, ...
        state: default, hover, pressed, disabled, ...
            when state is default, it can be omitted.
    examples:
        button_bg
        button_bg_hover
        button_bg_pressed
        text_main
        text_main_disabled
        text_hint
        text_link
"""
import re

from .base import Base
from .base import T


class Color(Base):
    _similar_states = (
        ('default', 'enabled', 'normal'),
        ('active', 'chosen', 'focused', 'hovered', 'pressed', 'selected'),
        ('disabled', 'inactive'),
    )
    _valid_states = tuple(y for x in _similar_states for y in x)
    # _valid_states = (
    #     'active', 'default', 'disabled', 'enabled', 'focused', 'hovered',
    #     'inactive', 'normal', 'pressed', 'selected',
    # )
    
    def _normalize(self, data: T.Data) -> T.Data:
        digitail = re.compile(r'([a-zA-Z_]+)(\d+)$')
        for k, v in data:
            # if k == v:
            #     # e.g. {'black': 'black'}
            #     yield k + '_default', v
            if m := digitail.search(k):
                # e.g. {'black_5': '#393355',
                #       'black5' : '#393355'}
                a, b = m.groups()
                k = a.rstrip('_') + '_' + b
                yield k, v
            elif '_' in k:
                # e.g. {'frame_bg_default' : '#F1F1F3',
                #       'frame_bg'         : '#F1F1F3',
                #       'button_bg_hovered': '#E9F0FB'}
                a, b = k.rsplit('_', 1)
                if b in self._valid_states:
                    yield k, v
                else:
                    yield k + '_default', v
            else:
                # e.g. {'active': '#E9F0FB',
                #       'text'  : '#393355'}
                yield k + '_default', v
    
    def _create_similars(self, data: T.Data) -> T.Data:
        resolved = set(k for k, _ in data)
        similar_states_dict = {
            y: x for x in self._similar_states for y in x
        }
        for k, v in data:
            if '_' in k:
                a, b = k.rsplit('_', 1)
                if b in similar_states_dict:
                    for c in similar_states_dict[b]:
                        if c != b:
                            if (k1 := f'{a}_{c}') not in resolved:
                                yield k1, v
                                resolved.add(k1)
                elif b.isdigit():  # e.g. 'red_7' -> 'red7'
                    if (k1 := f'{a}{b}') not in resolved:
                        yield k1, v
                        resolved.add(k1)
    
    def _shortify(self, data: T.Data) -> T.Data:
        for k, v in data:
            # if k.endswith(('_default', '_5')):
            #     yield k.rsplit('_', 1)[0], v
            if k.endswith('_default'):
                yield k[:-8], v
