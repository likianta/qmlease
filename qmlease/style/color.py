"""
# color naming style (proposal)

BEM naming style.

- B: block
  - comp: component
  - frame (undetermined, maybe changed to container)
  - text
  - theme
- E: element
  - bg
  - fg
  - border
  - shadow
  - ...
- M: modifier
  - default
  - hovered
  - pressed
  - enabled
  - disabled
  - selected
  - highlighted
  - ...

# examples

- comp_bg_default
- comp_bg_hovered
- comp_bg_pressed
- comp_border_default
- comp_border_hovered
- comp_border_pressed
- comp_border_selected
- comp_shadow_default
- comp_shadow_lighter
- comp_shadow_darker

- frame_bg_default
- frame_bg_lighter
- frame_bg_darker

- theme_blue_0
- theme_blue_1
- theme_blue_2
- ...
- theme_green_0
- theme_green_1
- theme_green_2
- ...

- text_text_default
- text_text_selected
- text_text_prompted
- text_text_highlighted
- text_text_warning, text_text_error
- text_text_success
- text_text_hint
- text_text_disabled
- text_selection_default
- text_cursor_default
"""
from ._base import Base


class Color(Base):
    
    def _get_abbrs(self, name: str):
        """
        rules:
            - if name starts with 'comp_' but not 'comp_bg_', strip 'comp_'
            - if name starts with 'text_', strip 'text_'
            - if name starts with 'theme_', strip 'theme_'
            - if name ends with '_0', strip '_0'
            - if name ends with '_default', strip '_default'
        """
        # strip head
        if name.startswith('comp_') and not name.startswith('comp_bg_'):
            yield name[5:]
        elif name.startswith('theme_'):
            yield name[6:]
        elif name.startswith('text_'):
            yield name[5:]
        
        # strip tail
        if name.endswith('_0'):
            yield name[:-2]
        elif name.endswith('_default'):
            yield name[:-8]
        elif name.endswith('_normal'):
            # DELETE: remove this. we won't use "normal" anymore, please use
            #   "default" instead.
            yield name[:-7]
        
        # strip both
        if name.startswith('theme_') and name.endswith('_0'):
            yield name[6:-2]
        elif not name.startswith('comp_bg_') and name.endswith('_default'):
            yield name.split('_')[-2]
