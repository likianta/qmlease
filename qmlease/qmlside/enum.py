from qtpy.QtQml import QQmlPropertyMap

from .._env import QT_VERSION


class Auto:
    
    def __init__(self, start: int = 0) -> None:
        self._counter = start
    
    def __call__(self) -> int:
        self._counter -= 1
        return self._counter


_auto = Auto()


class _Enum:
    # general
    AUTO = _auto()
    DEFAULT = _auto()
    NONE = _auto()
    ZERO = _auto()
    
    # justify
    AROUND = _auto()
    BETWEEN = _auto()
    CENTER = _auto()
    EVENLY = _auto()
    LEFT = _auto()
    RIGHT = _auto()
    
    # size
    FILL = _auto()
    HUG_CONTENT = _auto()
    SHRINK = _auto()
    STRETCH = _auto()
    WRAP = _auto()


class PyEnum(QQmlPropertyMap, _Enum):
    
    def __init__(self) -> None:
        super().__init__()
        if QT_VERSION >= 6.1:
            # since 6.1. this performs much faster than `insert(k, v)`.
            self.insert({
                k: v for k, v in _Enum.__dict__.items()
                if not k.startswith('_')
            })
            self.insert({
                k.lower(): v for k, v in _Enum.__dict__.items()
                if not k.startswith('_')
            })
        else:
            for k, v in _Enum.__dict__.items():
                if not k.startswith('_'):
                    self.insert(k, v)
                    self.insert(k.lower(), v)


pyenum = PyEnum()
