from qtpy.QtCore import QObject

from ...qtcore import Slot

strict_mode = False


class ResourceManager(QObject):
    
    @Slot(str, result=object)
    @Slot(str, dict, result=object)
    def get(self, name: str, kwargs: dict = None):
        return self._get(name, **(kwargs or {}))
    
    def _get(self, name, **kwargs):
        raise NotImplementedError
    
    def _fetch(self, name):
        assert hasattr(self, name)
        return getattr(self, name)


class BaseResourceManager(QObject):
    
    @Slot(str, result=str)
    def get(self, name: str) -> str:
        assert hasattr(self, name)
        return getattr(self, name)
