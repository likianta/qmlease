"""
fix typehint of Signal and Slot.
"""
from __future__ import annotations

import typing as t0
from functools import wraps
from typing import cast

# fix typehint of Signal and Slot.
# https://rednafi.github.io/reflections/static-typing-python-decorators.html
import typing_extensions as t1
from qtpy.QtCore import QObject
from qtpy.QtCore import Signal as OriginSignal
from qtpy.QtCore import Slot
from qtpy.QtQml import QJSValue

from .._env import QT_API

__all__ = ['signal', 'slot']

# hold some objects globally (elevate their refcount), to prevent python gc.
__hidden_ref = []


class T:
    ArgType0 = t0.Union[type, str]
    ArgType1 = type
    ParamSpec = t1.ParamSpec('ParamSpec')
    SlotReturn0 = t0.Optional[type]
    SlotReturn1 = t0.Union[str, type, None]
    
    Func = t0.Callable[ParamSpec, t0.Any]


def slot(*argtypes: T.ArgType0,
         name: str = '',
         result: T.SlotReturn0 = None) -> T.Func:
    """
    args:
        argtypes: see `def _reformat_argtypes()`.
        name: str
        result: see `def _reformat_result()`.
    """
    argtypes = _reformat_argtypes(argtypes)
    result = _reformat_result(result)
    
    def decorator(func: T.Func) -> T.Func:
        nonlocal argtypes, name, result
        if QT_API == 'pyqt5' and result is None:
            __hidden_ref.append(
                Slot(*argtypes,
                     name=(name or func.__name__))(func)
            )
        else:
            __hidden_ref.append(
                Slot(*argtypes,
                     name=(name or func.__name__),
                     result=result)(func)
            )
        
        @wraps(func)
        def func_wrapper(
                *args: T.ParamSpec.args,
                **kwargs: T.ParamSpec.kwargs
        ) -> T.Func:
            from .qobject import QObjectBaseWrapper
            new_args = []
            new_kwargs = {}
            
            for arg in args:
                if isinstance(arg, QJSValue):
                    new_args.append(arg.toVariant())
                elif isinstance(arg, QObject):
                    new_args.append(QObjectBaseWrapper(arg))
                else:
                    new_args.append(arg)
            
            for k, v in kwargs.items():
                if isinstance(v, QJSValue):
                    new_kwargs[k] = v.toVariant()
                elif isinstance(v, QObject):
                    new_kwargs[k] = QObjectBaseWrapper(v)
                else:
                    new_kwargs[k] = v
            
            return func(*new_args, **new_kwargs)
        
        return func_wrapper
    
    return decorator


def _reformat_argtypes(
        argtypes: t0.Tuple[T.ArgType0, ...]
) -> t0.Tuple[T.ArgType1, ...]:
    """
    mapping:
        # <group>:
        #   <input>: <output>  # <optional note>
        basic types:
            bool : bool
            bytes: bytes  # not tested!
            float: float
            int  : int
            str  : str
        object:
            QObject  : QObject
            object   : QObject
            'item'   : QObject
            'object' : QObject
            'qobject': QObject
        qjsvalue:
            dict      : QJSValue
            list      : QJSValue
            set       : QJSValue  # never used
            tuple     : QJSValue
            ...       : QJSValue
            'any'     : QJSValue
            'pyobject': QJSValue  # deprecated
            '...'     : QJSValue
        error:
            None   : None is not convertable!
            <other>: <other> is not convertable!
    """
    new_argtypes = []
    
    str_2_type = {
        'any'     : QJSValue,
        'item'    : QObject,
        'object'  : QObject,
        'pyobject': QJSValue,
        'qobject' : QObject,
        '...'     : QJSValue,
    }
    
    for t in argtypes:
        if isinstance(t, str):
            if t in str_2_type:
                t = str_2_type[t]
            else:
                raise Exception(f'Argtype `{t}` is not convertable!')
        elif t in (bool, bytes, float, int, str, QObject):
            pass
        elif t in (object,):
            t = QObject
        elif t in (dict, list, set, tuple):
            t = QJSValue
        else:
            raise Exception(f'Argtype `{t}` is not convertable!')
        new_argtypes.append(t)
    
    return tuple(new_argtypes)


def _reformat_result(result: T.SlotReturn0) -> T.SlotReturn1:
    """
    mapping:
        # <group>:
        #   <input>: <output>  # <optional note>
        basic types:
            None : None
            bool : bool
            bytes: bytes  # not tested!
            float: float
            int  : int
            str  : str
        qvariant:
            dict  : 'QVariant'
            list  : 'QVariant'
            object: 'QVariant'
            set   : 'QVariant'  # not tested!
            tuple : 'QVariant'
            ...   : 'QVariant'
        error:
            <other>: <other> is not convertable!
    """
    if result in (None, bool, bytes, float, int, str):
        return result
    if result in (dict, list, set, tuple, object, ...):
        return 'QVariant'
    raise Exception(f'Result `{result}` is not convertable!')


# -----------------------------------------------------------------------------

class Signal:
    
    def __call__(self, *argtypes: type): ...
    
    def connect(self, func): ...
    
    def emit(self, *args): ...


signal = cast(t0.Type[Signal], OriginSignal)
