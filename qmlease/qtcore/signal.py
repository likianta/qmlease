import typing as tp
# from lk_utils import Signal as LkSignal
from qtpy.QtCore import Signal as QtSignal
# from uuid import uuid1
# from ..application import hot_reloader


# class Signal:
#
#     def __class_getitem__(cls, *_: tp.Type) -> tp.Type['Signal']:
#         """
#         use square brackets to annotate a signal type.
#         [@ https://stackoverflow.com/a/68982326]
#         example:
#             class MyObject(QObject):
#                 my_signal: Signal[int, str]
#         """
#         return cls
#
#     def __init__(self, *args: tp.Type, **kwargs: tp.Type) -> None:
#         """
#         example:
#             sig1 = Signal(int, str)
#             @sig1.connect
#             def _foo(id: int, name: str) -> None:
#                 ...
#
#             sig2 = Signal(name=str, age=int)
#             @sig2.connect
#             def _bar(name: str, age: int) -> None:
#                 ...
#         """
#         self._qt_signal = QtSignal(*args, *kwargs.values())
#         # self._uid = uuid1().hex
#
#     def connect(self, func: tp.Callable) -> None:
#         self._qt_signal.connect(func)
#
#     def emit(self, *args: tp.Any, **kwargs: tp.Any) -> None:
#         self._qt_signal.emit(*args, *kwargs.values())


class SignalFactory:
    def __getitem__(self, *_: tp.Type) -> tp.Type[QtSignal]:
        return QtSignal
    
    def __call__(self, *args, **kwargs):
        return QtSignal(*args, *kwargs.values())


Signal = SignalFactory()


# def bind_signal(sig: Signal):
#     def wrapper(func: tp.Callable):
#         sig.connect(func)
#         return func
#     return wrapper
