from qtpy.QtQml import QQmlPropertyMap

from .._env import QT_VERSION


class _AutoCounter:
    def __init__(self, start: int = 0) -> None:
        self._counter = start

    def __call__(self) -> int:
        self._counter -= 1
        return self._counter


_count_down = _AutoCounter()


class _Enum:
    # general
    AUTO = _count_down()
    DEFAULT = _count_down()
    NONE = _count_down()
    ZERO = _count_down()

    # justify
    AROUND = _count_down()
    BETWEEN = _count_down()
    CENTER = _count_down()
    EVENLY = _count_down()
    LEFT = _count_down()
    RIGHT = _count_down()

    # size
    FILL = _count_down()
    HUG_CONTENT = _count_down()
    SHRINK = _count_down()
    STRETCH = _count_down()
    WRAP = _count_down()


class PyEnum(QQmlPropertyMap, _Enum):
    def __init__(self) -> None:
        super().__init__()
        if QT_VERSION >= (6, 1, 0):
            # since 6.1. this performs much faster than `insert(k, v)`.
            self.insert(
                {
                    k: v
                    for k, v in _Enum.__dict__.items()
                    if not k.startswith('_')
                }
            )
            self.insert(
                {
                    k.lower(): v
                    for k, v in _Enum.__dict__.items()
                    if not k.startswith('_')
                }
            )
        else:
            for k, v in _Enum.__dict__.items():
                if not k.startswith('_'):
                    self.insert(k, v)
                    self.insert(k.lower(), v)


pyenum = PyEnum()
