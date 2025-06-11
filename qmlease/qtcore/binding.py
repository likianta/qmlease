"""
copied from lambda_ex.grafting
"""
import typing as t
from functools import partial

from qtpy.QtCore import QObject
from qtpy.QtCore import Signal

_grafted = set()


class T:
    AsIs = t.TypeVar('AsIs', bound=t.Callable)


def bind(trigger: T.AsIs, *args, emit_now: bool = False, **kwargs) -> T.AsIs:
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


def bind_prop(
    emitter: QObject,
    emitter_prop: str,
    receiver: t.Optional[QObject] = None,
    receiver_prop: t.Optional[str] = None,
    custom_handler: t.Callable = None,
    effect_now: bool = False,
) -> None:
    if receiver is None:
        receiver = emitter
        assert receiver_prop
    else:
        if receiver_prop is None:
            receiver_prop = emitter_prop
    
    def _default_handler():
        receiver.setProperty(receiver_prop, emitter.property(emitter_prop))
    
    handler = custom_handler or _default_handler
    
    getattr(emitter, f'{emitter_prop}Changed').connect(handler)
    
    if effect_now:
        handler()


def bind_signal(signal: T.AsIs, emit_now: bool = False) -> T.AsIs:
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
    eval(
        'qobj.{signal}.connect(func)'.format(signal=signal),
        {'qobj': qobj, 'func': func}
    )
