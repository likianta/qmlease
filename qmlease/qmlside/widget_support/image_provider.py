"""
ref:
    https://doc.qt.io/qt-6/qml-qtquick-image.html#source-prop
    https://doc.qt.io/qt-6/qquickimageprovider.html
        https://doc.qt.io/qt-6/qquickimageprovider.html#an-example
"""

import atexit
import typing as t
from lk_utils import fs
from qtpy.QtCore import QSize
from qtpy.QtGui import QImage
from qtpy.QtQuick import QQuickImageProvider
from uuid import uuid1
from ...qtcore import QObject
from ...qtcore import signal


class T:
    BakedImage = t.TypeVar('BakedImage', bound=t.Any)


class LocalImageProvider(QObject):
    image_updated = signal(str)
    
    def __init__(self, root: str = fs.xpath('_cache')) -> None:
        super().__init__()
        self.root = fs.abspath(root)
        self._cached_files = []
        atexit.register(self._clear_cache)
    
    def render(self, *args, **kwargs) -> str:
        file = self._save_to_local(self._bake_image(*args, **kwargs))
        self._cached_files.append(file)
        self.image_updated.emit(file)
        return file
    
    def _bake_image(self, *args, **kwargs) -> T.BakedImage:
        """
        example:
            chart = alt.Chart(...)
            return chart
        """
        raise NotImplementedError
    
    def _clear_cache(self) -> None:
        for f in self._cached_files:
            fs.remove_file(f)
    
    def _random_file(self) -> str:
        return '{}/{}.png'.format(self.root, uuid1())
    
    def _save_to_local(self, obj: T.BakedImage) -> str:
        """
        example:
            file = self._random_file()
            obj.save(file, 'png')
            return file
        """
        raise NotImplementedError


# FIXME
class ImageProvider(QQuickImageProvider):
    def __init__(
        self,
        domain: str = 'myimages',
        default_size: t.Tuple[int, int] = (800, 600),
        #   TODO: dynamically get size from realtime image data.
    ) -> None:
        super().__init__(QQuickImageProvider.ImageType.Image)
        self._default_size = default_size
        self._domain = domain
        self._image_pool = {}  # {id: bytes, ...}
        self._simple_counter = 0
        
        from ...application import app
        app.engine.addImageProvider(self._domain, self)
    
    @property
    def domain(self) -> str:
        return self._domain
    
    # @property
    # def last_image(self) -> t.Optional[QImage]:
    #     if self._image_pool:
    #         assert len(self._image_pool) == 1
    #         for only_one in self._image_pool.values():
    #             return QImage(
    #                 only_one, 800, 600, QImage.Format.Format_RGBA8888
    #             )
    
    @property
    def url_prefix(self) -> str:
        return 'image://{}'.format(self._domain)
    
    def form_url(self, id: str) -> str:
        return 'image://{}/{}'.format(self._domain, id)
    
    def render(self, *args, **kwargs) -> str:
        self._simple_counter += 1
        id = str(self._simple_counter)
        self._image_pool[id] = self._bake_image(*args, **kwargs)
        return self.form_url(id)
    
    def requestImage(self, id: str, size: QSize, req_size: QSize) -> QImage:
        print(id, type(id), size, req_size, ':v')
        png_data = self._image_pool.pop(id)
        img = QImage(
            png_data,
            req_size.width() or self._default_size[0],
            req_size.height() or self._default_size[1],
            QImage.Format.Format_RGBA8888,
        )
        return img
    
    def _bake_image(self, *args, **kwargs) -> bytes:
        """
        example:
            chart = alt.Chart(...)
            with io.BytesIO() as f:
                chart.save(f, 'png')
                f.seek(0)
                return f.read()
        """
        raise NotImplementedError
