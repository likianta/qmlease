"""
copied from lambda_ex.grafting
"""
import typing as t
from functools import partial
from typing import Callable

from qtpy.QtCore import QObject
from qtpy.QtCore import Signal

_grafted = set()


def bind(trigger: Callable, *args, emit_now=False, **kwargs) -> Callable:
    def decorator(func):
        uid = (id(trigger), id(func))
        if uid in _grafted:
            return func
        _grafted.add(uid)
        if args or kwargs:
            trigger(partial(func, *args, **kwargs))
        else:
            trigger(func)
        if emit_now:
            func(*args, **kwargs)
        return func
    
    return decorator


def bind_signal(signal: Callable, emit_now=False) -> Callable:
    assert isinstance(signal, Signal)
    
    def decorator(func):
        uid = (id(signal), id(func))
        if uid in _grafted:
            return func
        _grafted.add(uid)
        signal.connect(func)  # noqa
        if emit_now:
            # signal.emit()
            func()  # FIXME: what about args and kwargs?
        return func
    
    return decorator


# TODO: experimental
def bind_func(qobj: QObject, signal: str, func: t.Callable) -> None:
    eval('qobj.{signal}.connect(func)'.format(signal=signal),
         {'qobj': qobj, 'func': func})
