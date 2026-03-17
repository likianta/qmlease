import typing as tp
from functools import wraps
from types import EllipsisType
from types import NoneType

# fix typehint of Signal and Slot.
# https://rednafi.github.io/reflections/static-typing-python-decorators.html
from qtpy.QtCore import QObject as QtObject
from qtpy.QtCore import Slot as QtSlot
from qtpy.QtQml import QJSValue

from .._env import QT_API

# hold some objects globally (elevate their refcount), to prevent python gc.
__hidden_ref = []


class T:
    ArgType0 = tp.Union[type, str]
    ArgType1 = type
    ParamSpec = tp.ParamSpec('ParamSpec')
    SlotReturn0 = tp.Union[NoneType, tp.Type, EllipsisType]
    SlotReturn1 = tp.Union[str, type, None]
    Func = tp.Callable[ParamSpec, tp.Any]


# noinspection PyPep8Naming
def Slot(
    *argtypes: T.ArgType0,
    name: str = '',
    result: T.SlotReturn0 = None
) -> T.Func:
    """
    example:
        @slot(str, int, object)
        def foo(msg: str, flag: int, item: QObject):
            ...

        @slot(result=bool)
        def bar() -> bool:
            ...

    valid types in slot(..., result=...):
                        ^^^         ^^^
        see `_reformat_argtypes : docstring`
    """
    argtypes = _reformat_argtypes(argtypes)
    result = _reformat_result(result)
    
    def decorator(func: T.Func) -> T.Func:
        nonlocal argtypes, name, result
        if QT_API == 'pyqt5' and result is None:
            __hidden_ref.append(
                QtSlot(
                    *argtypes,
                    name=(name or func.__name__)
                )(func)
            )
        else:
            __hidden_ref.append(
                QtSlot(
                    *argtypes,
                    name=(name or func.__name__),
                    result=result
                )(func)
            )
        
        @wraps(func)
        def func_wrapper(
            *args: T.ParamSpec.args,
            **kwargs: T.ParamSpec.kwargs
        ) -> T.Func:
            from .qobject import QObjectDelegate
            from ..qmlside import Model
            new_args = []
            new_kwargs = {}
            
            for arg in args:
                if isinstance(arg, QJSValue):
                    new_args.append(arg.toVariant())
                elif isinstance(arg, QtObject) and not isinstance(arg, Model):
                    new_args.append(QObjectDelegate(arg))
                else:
                    new_args.append(arg)
            
            for k, v in kwargs.items():
                if isinstance(v, QJSValue):
                    new_kwargs[k] = v.toVariant()
                elif isinstance(v, QtObject) and not isinstance(v, Model):
                    new_kwargs[k] = QObjectDelegate(v)
                else:
                    new_kwargs[k] = v
            
            return func(*new_args, **new_kwargs)
        
        return func_wrapper
    
    return decorator


def _reformat_argtypes(
    argtypes: tp.Tuple[T.ArgType0, ...]
) -> tp.Tuple[T.ArgType1, ...]:
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
        'item'    : QtObject,
        'object'  : QtObject,
        'pyobject': QJSValue,
        'qobject' : QtObject,
        '...'     : QJSValue,
    }
    
    for t in argtypes:
        if isinstance(t, str):
            if t in str_2_type:
                t = str_2_type[t]
            else:
                raise Exception(f'Argtype `{t}` is not convertable!')
        elif t in (bool, bytes, float, int, str, QtObject):
            pass
        elif t in (object,):
            t = QtObject
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
