import re

from .base import ResourceManager
from .base import strict_mode


class Patterns:
    p0 = re.compile(r'#(?:[A-Z][a-z]+)+([0-9]*)')
    #                  ^1-------------^^2-----^
    #   1: main name (multi words)
    #   2: degree
    p1 = re.compile(r'((?:[A-Z][a-z]+)+)([A-Z][a-z]+)$')
    #                 ^1---------------^^2-----------^
    #   1: main name (multi words)
    #   2: state (single word)
    p2 = re.compile(r'[A-Z][a-z]+')
    #   word in name. use `findall` to get all words from name.


class ColorResourceManager(ResourceManager):
    
    def _get(self, name: str, **kwargs) -> str:
        if not hasattr(self, name):
            color = self._main(name)
            setattr(self, name, color)
        return getattr(self, name)
    
    def _main(self, name: str, **kwargs):
        if kwargs.get('check_degree', True):
            name, degree = Patterns.p0.search(name).groups()
            if degree:
                degree = int(degree)
                assert 0 <= degree < 100
                if strict_mode: assert degree % 25 == 0
                return '#{:0>2d}{}'.format(
                    degree, self._main(name, check_degree=False)[1:]
                )
        
        if kwargs.get('check_state', True):
            if m := Patterns.p1.search(name):
                name, state = m.groups()
                if state in (
                        'Accent', 'Dark', 'Deep', 'Light', 'Normal',
                ):
                    pass
                else:
                    return self._fetch(name) + state
        
        return self._fetch(name)
