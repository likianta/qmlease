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

from ._base import Base


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
    
    def _normalize(self, data: dict) -> dict:
        new_data = {}
        digit_tail = re.compile(r'([a-zA-Z_]+)(\d+)$')
        for k, v in data.items():
            if k == v:
                # e.g. {'black': 'black'}
                k = k + '_default'
                new_data[k] = v
            elif m := digit_tail.search(k):
                # e.g. {'black_5': '#393355',
                #       'black5' : '#393355'}
                a, b = m.groups()
                k = a.rstrip('_') + '_' + b
                new_data[k] = v
            elif '_' not in k:
                # e.g. {'active': '#E9F0FB',
                #       'text'  : '#393355'}
                if k in self._valid_states:
                    k = 'common_' + k
                else:
                    k = k + '_default'
                new_data[k] = v
            else:
                # e.g. {'frame_bg_default' : '#F1F1F3',
                #       'frame_bg'         : '#F1F1F3',
                #       'button_bg_hovered': '#E9F0FB'}
                a, b = k.rsplit('_', 1)
                if b in self._valid_states:
                    new_data[k] = v
                else:
                    k = k + '_default'
                    new_data[k] = v
        return new_data
    
    def _create_similars(self, data: dict) -> dict:
        new_data = {}
        resolved = set()
        similar_states_dict = {
            y: x for x in self._similar_states for y in x
        }
        for k, v in data.items():
            if k in resolved:
                continue
            if '_' in k:
                a, b = k.rsplit('_', 1)
                if b in similar_states_dict:
                    for c in similar_states_dict[b]:
                        if c != b:
                            if f'{a}_{c}' not in data:
                                new_data[f'{a}_{c}'] = v
                            resolved.add(f'{a}_{c}')
            resolved.add(k)
        return new_data
    
    def _shortify(self, data: dict) -> dict:
        new_data = {}
        for k, v in data.items():
            if k.startswith('common_') and k.endswith('_default'):
                new_data[k[7:]] = v
                new_data[k[7:-8]] = v
                new_data[k[:-8]] = v
                continue
            else:
                if k.startswith('common_'):
                    new_data[k[7:]] = v
                    continue
                elif k.endswith('_default'):
                    new_data[k[:-8]] = v
                    continue
            if k.endswith('_5'):
                new_data[k[:-2]] = v
        return new_data
