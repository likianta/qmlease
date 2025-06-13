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
    *args: t.Union[QObject, str, bool],
    # emitter: QObject,
    # emitter_prop: str,
    # receiver: t.Optional[QObject] = None,
    # receiver_prop: t.Optional[str] = None,
    custom_handler: t.Callable = None,
    effect_now: bool = False,
) -> None:
    """
    args form:
        1. (receiver, receiver_prop, emitter_prop)
        2. (receiver, receiver_prop, emitter_prop, effect_now)
        3. (receiver, receiver_prop, emitter)
        4. (receiver, receiver_prop, emitter, effect_now)
        5. (receiver, receiver_prop, emitter, emitter_prop)
        6. (receiver, receiver_prop, emitter, emitter_prop, effect_now)
        
    examples:
        bind_prop(item, 'width', 'height')
            when item height changed, update width equal to height.
        bind_prop(child, 'width', parent)
            when parent width changed, update child width equal to parent's.
        bind_prop(child, 'width', parent, 'height')
            when parent height changed, update child width equal to parent's.
        bind_prop(child, 'width', parent, 'height', True)
            same like above, but trigger the change event right now.
    """
    assert len(args) in (3, 4, 5)
    args += (None, None)
    receiver = args[0]
    receiver_prop = args[1]
    if isinstance(args[2], str):  # 1.2.
        emitter = receiver
        emitter_prop = args[2]
        if isinstance(args[3], bool):  # 2.
            effect_now = args[3]
    else:  # 3.4.5.6.
        emitter = args[2]
        if args[3] is None:  # 3.
            emitter_prop = receiver_prop
        elif isinstance(args[3], bool):  # 4.
            emitter_prop = receiver_prop
            effect_now = args[3]
        else:  # 5.6.
            emitter_prop = args[3]
            if isinstance(args[4], bool):  # 6.
                effect_now = args[4]
    if receiver_prop == emitter_prop:
        assert receiver is not emitter
    
    def default_handler() -> None:
        receiver.setProperty(receiver_prop, emitter.property(emitter_prop))
    
    handler = custom_handler or default_handler
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
