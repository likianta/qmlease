from qtpy.QtCore import QObject

from ...qtcore import slot

strict_mode = False


class ResourceManager(QObject):
    
    @slot(str, result=object)
    @slot(str, dict, result=object)
    def get(self, name: str, kwargs: dict = None):
        return self._get(name, **(kwargs or {}))
    
    def _get(self, name, **kwargs):
        raise NotImplementedError
    
    def _fetch(self, name):
        assert hasattr(self, name)
        return getattr(self, name)


class BaseResourceManager(QObject):
    
    @slot(str, result=str)
    def get(self, name: str) -> str:
        assert hasattr(self, name)
        return getattr(self, name)
