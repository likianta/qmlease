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
import typing as t

from ._base import Base


class Color(Base):
    _familiar_states = (
        ('default', 'enabled', 'normal'),
        ('active', 'focused', 'hovered', 'pressed', 'selected'),
        ('disabled',),
    )
    
    def _post_complete(self, data: dict) -> dict:
        state_words = tuple(y for x in self._familiar_states for y in x)
        processed = set()
        inflated_count = 0
        
        for name, value in tuple(data.items()):
            if '_' in name:
                a, b = name.rsplit('_', 1)
                if b not in state_words:
                    a, b = name, 'default'
                    data[f'{a}_{b}'] = value
            else:
                a, b = name, 'default'
                data[f'{a}_{b}'] = value
            
            for a in processed:
                continue
            for c in self._find_familiar_state(b):
                if f'{a}_{c}' not in data:
                    data[f'{a}_{c}'] = value
                    inflated_count += 1
            processed.add(a)
        
        # if inflated_count:
        #     print(':v', 'increased {} items'.format(inflated_count))
        
        return data
    
    def _find_familiar_state(self, state: str) -> t.Iterator[str]:
        for x in self._familiar_states:
            if state in x:
                for y in x:
                    if y != state:
                        yield y
