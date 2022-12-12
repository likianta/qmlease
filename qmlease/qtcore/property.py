from __future__ import annotations

import typing as t

from qtpy.QtCore import Property as PropertyBase
from qtpy.QtCore import QObject
from qtpy.QtCore import SignalInstance

from .signal_slot import signal


class AutoProp:
    """ this is a dataclass-like class, just store some info for later used by
        `.qobject.DynamicSignalMeta.__new__` """
    const: bool
    default: t.Any
    notify: bool
    type_: type
    
    def __init__(self, value: t.Any, type_: type = None,
                 notify: bool = 'auto', const=False):
        """
        note: the `notify` is generally used for primitive types, like `int`,
            `float`, `str`, etc. if you are passing a mutable object, e.g. a
            `QModel` instance, you should set it False and use `QModel`'s own
            signal.
        """
        self.default = value
        self.type_ = type_ or type(value)
        if notify == 'auto':
            if const:
                notify = False
            elif self.type_ in (bool, float, int, str):
                notify = True
            else:
                notify = False
        else:
            assert isinstance(notify, bool)
        self.notify = notify
        self.const = const


# -----------------------------------------------------------------------------
# FIXME or DELETE

class ValueHolder(QObject):  # TEST
    
    def __init__(self, value: t.Any, final_type: type):
        super().__init__()
        self._value = value
        self.value_changed = signal(final_type)
        # self._notifier = notifier
        # self.value_changed = notifier
    
    def get_value(self):
        return self._value
    
    def set_value(self, new: t.Any) -> None:
        if self._value != new:
            self._value = new
    
    # @property
    # def value_changed(self) -> signal | None:
    #     return self._notifier


class Property(PropertyBase):
    """
    see feature introduction in `.qobject.QObject : class-level docstring`.
    """
    type_: type
    _core: QObject
    _value: t.Any
    value_changed: signal | None
    
    def __init__(self, value: t.Any, *types: type | str):
        assert 0 <= len(types) <= 3
        #   possible types:
        #       ()  # nothing. it is same with `('auto',)`
        #       (int, )  # or str, bool, float, ...
        #       (int, 'const')
        #       (int, 'final')
        #       (int, 'const', 'final')
        #       ('auto', )
        #       ('auto', 'const')
        #       ('auto', 'final')
        #       ('auto', 'const', 'final')
        
        self._value = value
        
        auto = 'auto' in types if types else True
        const = 'const' in types
        final = 'final' in types
        if auto:
            final_type = self._auto_detect_type(value)
        else:
            # assert len(types) > 0
            assert types[0] in (bool, float, int, str)
            final_type = types[0]
        self.type_ = final_type
        
        # if not const and not final:
        #     self.value_changed = signal(final_type)
        # else:
        #     self.value_changed = None
        if not const and not final:
            self.value_changed = SignalInstance()
            self.value_changed = ValueHolder(value, final_type).value_changed
        else:
            self.value_changed = None
        
        super().__init__(
            final_type,
            self.get_value,
            self.set_value,
            # notify=self.value_changed,
            constant=const, final=final,
        )
        
        # value_holder = ValueHolder(value, (
        #     signal(final_type) if (not const and not final) else None
        # ))
        # super().__init__(
        #     final_type,
        #     value_holder.get_value,
        #     value_holder.set_value,
        #     notify=value_holder.value_changed,
        #     constant=const, final=final,
        # )
    
    def set_core(self, qobj: QObject) -> None:
        self._core = qobj
    
    def get_value(self) -> t.Any:
        return self._value
    
    def set_value(self, new: t.Any, xxx) -> None:
        print('part 1', new, ':vs')
        print('part 2', xxx, ':vs')
        if self._value != new:
            self._value = new
            if self.value_changed:
                self.value_changed.emit(new)
    
    @staticmethod
    def _auto_detect_type(value: t.Any) -> type:
        """
        support only basic types.
        """
        out = type(value)
        assert out in (bool, float, int, str)
        return out
