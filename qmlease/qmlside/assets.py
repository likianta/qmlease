import typing as tp
from inspect import currentframe
from os import getcwd
from os.path import dirname
from types import FrameType

from lk_utils import fs

from ..qtcore import QObject
from ..qtcore import Slot

class T:
    PathUrl = str  # a 'file:///' url to a file or directory


class Assets(QObject):
    
    def __init__(self) -> None:
        super().__init__()
        self._cwd = 'file:///' + getcwd().replace('\\', '/')
        self._src = self._cwd
        self._custom_sources = {}  # type: dict[str, str]
    
    def set_root(self, dir: str) -> None:
        self._src = 'file:///' + fs.abspath(dir)
    
    def add_source(self, src_dir: str, name: str = None) -> None:
        if name is None:
            name = fs.basename(src_dir)
        self._custom_sources[name] = 'file:///' + fs.abspath(src_dir)
    
    @Slot(result=str)
    @Slot(str, result=str)
    def src(self, relpath: str = '') -> str:
        if relpath == '':
            return self._src
        else:
            return fs.normpath(f'{self._src}/{relpath}')
    
    @Slot(result=str)
    @Slot(str, result=str)
    def cwd(self, relpath: str = '') -> str:
        if relpath == '':
            return self._cwd
        else:
            return fs.normpath(f'{self._cwd}/{relpath}')
    
    def here(self, relpath: str) -> T.PathUrl:
        last_frame: FrameType = currentframe().f_back  # type: ignore
        last_dir = dirname(last_frame.f_code.co_filename)
        return 'file:///' + fs.normpath(f'{last_dir}/{relpath}')

    @Slot(str, result=str)
    @Slot(str, str, result=str)
    def get(self, src_name: str, relpath: str = '') -> str:
        return fs.normpath(f'{self._custom_sources[src_name]}/{relpath}')


pyassets = Assets()
