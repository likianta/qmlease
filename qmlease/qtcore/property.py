from __future__ import annotations

import typing as t

from qtpy.QtCore import QObject


class T:
    Key = str  # should be a snake_case name.
    Val = t.Any
    InitProps = t.Dict[Key, t.Union[
        type,
        t.Tuple[type],
        t.Tuple[type, Val],
        t.Tuple[type, Val, bool]
    ]]


class PObject(QObject):
    
    def __init__(self):
        from functools import partial
        from qtpy.QtCore import Property
        from qtpy.QtCore import Signal
        
        self._props = {}
        
        for k, v in self._init_props().items():
            if isinstance(v, tuple):
                if len(v) == 1:
                    type_ = v[0]
                    value = None
                    is_constant = False
                elif len(v) == 2:
                    type_ = v[0]
                    value = v[1]
                    is_constant = False
                elif len(v) == 3:
                    type_ = v[0]
                    value = v[1]
                    is_constant = v[2]
                else:
                    raise Exception('invalid value format', (k, v))
            else:
                type_ = v
                value = None
                is_constant = False
            signal = Signal(type_)
            
            self._props[k] = value
            self._props[k + '_changed'] = signal
            
            # Property(<type>, <getter>, <setter>, constant=<bool>)
            prop = Property(
                type_,
                partial(self.get_prop, k),
                partial(self.set_prop, k),
                constant=is_constant,
                notify=signal
            )
            setattr(self.__class__, k, prop)
        
        super().__init__(None)
    
    def get_prop(self, k: T.Key) -> t.Any:
        return self._props[k]
    
    def set_prop(self, k: T.Key, v: T.Val) -> None:
        assert k in self._props
        self._props[k] = v
    
    def connect_(self, k: T.Key, func: t.Callable) -> None:
        self._props[k + '_changed'].connect(func)
    
    def notify(self, k: T.Key) -> None:
        self._props[k + '_changed'].emit(self._props[k])
    
    def _init_props(self) -> T.InitProps:
        """
        return: dict[str key, any val]
            key:
                property name, the name format should be a snake_case.
                warning: the name should not be ended with '_changed'.
            val:
                the value is either a type or a tuple object.
                when it is a type, for example:
                    {'name': str, 'age': int}
                when it is a tuple, it contains one to three elements:
                    {'name': (str,),
                     'age': (int, 21),
                     'height': (int, 21, True)}
                the first is type, second is init value, third is whether is it
                constant (default False).
                in most cases, we use `type` or `(type, init_value)` format.
        """
        raise NotImplementedError
    
    def __getitem__(self, item) -> T.Val:
        return self._props[item]
    
    def __setitem__(self, key, value) -> None:
        self.set_prop(key, value)
        self.notify(key)
