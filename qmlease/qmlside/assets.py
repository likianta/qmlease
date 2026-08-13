import typing as tp
from inspect import currentframe
from os import getcwd
from os.path import dirname
from types import FrameType

from lk_utils import fs

from ..qtcore import QObject
from ..qtcore import Slot


class T:
    AnyDirPath = str


class Assets(QObject):
    """
    usage:
        assets = Assets()

        assets.get('/aaa.png')
        # -> 'file:///<cwd>/aaa.png'

        assets.get('./bbb.png')
        # -> 'file:///<the_caller_directory>/bbb.png'

        assets.get('../ccc.png')
        # -> 'file:///<the_parent_directory_of_caller>/ccc.png'

        assets.add_source('/path/to/lkwidgets/assets', 'lkwidgets')
        assets.get('lkwidgets:/home.svg')
        # -> 'file:///path/to/lkwidgets/assets/home.svg'
    """

    def __init__(self) -> None:
        super().__init__()
        self._cwd = getcwd().replace('\\', '/')
        self._default = self._cwd
        self._sources = {}

    def set_default_source(self, dir: T.AnyDirPath) -> None:
        self._default = fs.abspath(dir)

    def add_source(
        self, dir: T.AnyDirPath, name: tp.Optional[str] = None
    ) -> None:
        self._sources[name or fs.basename(dir)] = fs.abspath(dir)

    @Slot(str, result=str)
    def get(self, relpath: str) -> str:
        if relpath.startswith(('./', '../')):
            caller_frame: FrameType = currentframe().f_back  # type: ignore
            caller_dir = dirname(caller_frame.f_code.co_filename)
            return 'file:///' + fs.normpath(f'{caller_dir}/{relpath}')
        elif relpath.startswith('/'):
            return 'file:///' + self._default + relpath
        else:
            a, b = relpath.split(':', 1)
            return 'file:///' + self._sources[a] + b


assets = Assets()
