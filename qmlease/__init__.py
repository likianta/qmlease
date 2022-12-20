if 1:  # step1: setup lk_logger
    import lk_logger
    lk_logger.setup(quiet=True)

if 2:  # step2: select qt api
    from ._env import QT_API

from .application import Application
from .application import app
from .pyside import pyside
from .pyside import register
from .qmlside import Model
from .qmlside import eval_js
from .qmlside import pyassets
from .qmlside import qlogger
from .qmlside import qml_eval
from .qmlside.widgets_backend import util
from .qtcore import AutoProp
from .qtcore import QObject
from .qtcore import bind
from .qtcore import bind_signal
from .qtcore import signal
from .qtcore import slot
from .style import pystyle

__version__ = '3.0.2'
