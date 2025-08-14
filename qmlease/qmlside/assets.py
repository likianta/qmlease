from os import getcwd

from lk_utils import fs

from ..qtcore import QObject
from ..qtcore import slot


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
    
    @slot(result=str)
    @slot(str, result=str)
    def src(self, relpath: str = '') -> str:
        if relpath == '':
            return self._src
        else:
            return fs.normpath(f'{self._src}/{relpath}')
    
    @slot(result=str)
    @slot(str, result=str)
    def cwd(self, relpath: str = '') -> str:
        if relpath == '':
            return self._cwd
        else:
            return fs.normpath(f'{self._cwd}/{relpath}')
    
    @slot(str, result=str)
    @slot(str, str, result=str)
    def get(self, src_name: str, relpath: str = '') -> str:
        return fs.normpath(f'{self._custom_sources[src_name]}/{relpath}')


pyassets = Assets()
