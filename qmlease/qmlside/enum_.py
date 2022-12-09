from qtpy.QtQml import QQmlPropertyMap


class Auto:
    
    def __init__(self):
        self._counter = 0
    
    def __call__(self) -> int:
        self._counter -= 1
        return self._counter


_auto = Auto()


class _Enum:
    # general
    AUTO = _auto()
    DEFAULT = _auto()
    NONE = _auto()
    
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
    
    def __init__(self):
        super().__init__(None)
        self.insert({k: v for k, v in _Enum.__dict__.items()
                     if not k.startswith('_')})  # noqa


pyenum = PyEnum()
