if 1:
    import lk_logger
    lk_logger.setup(quiet=True)

if 2:
    import signal
    import sys
    if sys.platform == 'win32':
        # fix `ctrl+c` to correctly kill process on windows.
        # https://stackoverflow.com/a/37420223/9695911
        signal.signal(signal.SIGINT, signal.SIG_DFL)

if 3:
    from ._env import QT_API
    from ._env import QT_VERSION

if 4:
    from .application import Application
    from .application import app

if 5:
    from . import qtcore
    from . import widgets
    from .pyside import pyside
    from .pyside import register
    from .qmlside import ListModel
    from .qmlside import Model  # DELETE?
    from .qmlside import SimpleModel  # DELETE?
    from .qmlside import eval_js
    from .qmlside import pyassets
    from .qmlside import console
    from .qmlside import qml_eval
    from .qmlside import widgets_backend
    from .qmlside.widgets_backend import log
    from .qmlside.widgets_backend import logger
    from .qmlside.widgets_backend import util
    from .qtcore import Property
    from .qtcore import QObject
    from .qtcore import Signal
    from .qtcore import Slot
    from .qtcore import bind
    from .qtcore import bind_prop
    from .qtcore import bind_signal
    from .style import pyenum
    from .style import pystyle
    from .widget_support import widget_support

__version__ = '4.0.0'
