"""
watchdog ref: https://dev.to/stokry/monitor-files-for-changes-with-python-1npj
"""
import os.path
import typing as t
from time import sleep

from lk_utils import fs
from lk_utils import new_thread
from lk_utils.filesniff.finder import _DefaultFilter  # noqa
from lk_utils.filesniff.finder import _default_filter  # noqa
from watchdog.events import FileModifiedEvent
from watchdog.events import FileSystemEventHandler

# https://github.com/gorakhargosh/watchdog/issues/93#issuecomment-547677667
# # from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver as Observer


class T:
    Call = t.Callable[[str], t.Any]
    # Call = t.Union[
    #     t.Callable[[], t.Any],
    #     t.Callable[[str], t.Any],
    #     t.Callable[[str, str], t.Any],
    # ]
    Filter = _DefaultFilter


class Path:
    isdir: bool
    path: str
    recursive: bool
    suffix: t.Tuple[str, ...]
    _call: t.Callable[[str], t.Any]
    
    def __init__(
        self,
        path: str,
        call: t.Callable[[str], t.Any],
        suffix: t.Tuple[str, ...] = (),
        recursive: bool = False,
    ):
        assert os.path.exists(path)
        if recursive:
            assert os.path.isdir(path)
        self.path = fs.abspath(path)
        self.isdir = os.path.isdir(path)
        self.recursive = recursive
        self.suffix = suffix
        self._call = call
    
    @property
    def call(self) -> t.Callable:
        return self
    
    def __call__(self, path: str) -> t.Any:
        if self.suffix and not path.endswith(self.suffix): return
        if (
            self.isdir
            and not self.recursive
            and dir[len(self.path) + 1 :].count('/') > 0
        ):
            return
        print(path)
        return self.call(path)


def watch_file_changes(
    *paths: Path,
    entrance: str = None,
    filter: t.Optional[T.Filter] = _default_filter,
) -> None:
    if entrance is None:
        # entrance = os.getcwd()
        entrance = os.path.commonpath(tuple(fs.dirpath(x.path) for x in paths))
    print(entrance)
    
    observer = Observer()
    handler = FilesListener(*paths, filter=filter)
    
    for p in paths:
        print(':i2sp', 'add to watch', p.path + (p.recursive and '/*' or ''))
        observer.schedule(handler, p.path, recursive=p.recursive)
    
    _start_polling(observer)


class FilesListener(FileSystemEventHandler):
    def __init__(
        self, *paths: Path, filter: t.Optional[T.Filter] = None
    ) -> None:
        super().__init__()
        self._file_2_call = {}
        self._dir_2_call = {}
        self._filter = filter
        for p in paths:
            if p.isdir and not p.suffix:
                self._dir_2_call[p.path + '/'] = p.call
            else:
                self._file_2_call[p.path + '/'] = p.call
    
    def on_modified(self, event: FileModifiedEvent) -> None:
        src_path = fs.normpath(event.src_path)
        print(src_path, os.path.getmtime(src_path), ':v')
        
        if self._filter:
            if event.is_directory:
                if (
                    self._filter.filter_dir(src_path, fs.basename(src_path))
                    is False
                ):
                    return
            else:
                if (
                    self._filter.filter_file(src_path, fs.basename(src_path))
                    is False
                ):
                    return
        
        if event.is_directory:
            for p, call in self._dir_2_call.items():
                if (src_path + '/').startswith(p):
                    call(src_path)
        else:
            for p, call in self._file_2_call.items():
                if (src_path + '/').startswith(p):
                    call(src_path)


@new_thread()
def _start_polling(observer: Observer) -> None:
    print('start file watcher. you can press `ctrl + c` to stop it.', ':p2')
    observer.start()
    try:
        while True:
            sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
        print('watchdog stopped')
    finally:
        observer.join()
