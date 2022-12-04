from lk_utils import loads

from qmlease import QObject
from qmlease import slot


class StylesheetLoader(QObject):
    
    def __init__(self, path: str):
        super().__init__()
        self._path = path
        
    @slot(result=dict)
    def reload(self) -> dict:
        data_i: dict = loads(self._path)
        data_o = {}
        
        for k, v in data_i.items():
            if v.startswith('$'):
                continue
            data_o[k] = v[1:]
        
        return data_o
