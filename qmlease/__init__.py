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

from .application import Application
from .application import app
from .pyside import pyside
from .pyside import register
from .qmlside import Model
from .qmlside import SimpleModel
from .qmlside import eval_js
from .qmlside import pyassets
from .qmlside import console
from .qmlside import qml_eval
from .qmlside import widgets_backend
from .qmlside import widget_support
from .qmlside.widgets_backend import log
from .qmlside.widgets_backend import logger
from .qmlside.widgets_backend import util
from .qtcore import AutoProp
from .qtcore import QObject
from .qtcore import bind
from .qtcore import bind_prop
from .qtcore import bind_signal
from .qtcore import signal
from .qtcore import slot
from .style import pyenum
from .style import pystyle

__version__ = '3.1.0'
