import typing as t

from lk_utils import load
from qtpy.QtQml import QQmlPropertyMap


class T:
    Data = t.Iterable[t.Tuple[str, t.Any]]


class Base(QQmlPropertyMap):
    data: dict
    
    def __init__(self) -> None:
        super().__init__()
        self.data = {}
    
    def __getitem__(self, item: str) -> t.Any:
        return self.data[item]
    
    def __setitem__(self, key: str, value: t.Any) -> None:
        self.data[key] = value
        self.insert(key, value)
    
    # -------------------------------------------------------------------------
    
    def update_from_file(self, file: str) -> None:
        self.update(load(file))
    
    def update(self, data: dict) -> None:
        plain_data = self._resolve_references(data)
        norml_data = tuple(self._normalize(plain_data))
        alias_data = tuple(self._create_similars(norml_data))
        short_data = tuple(self._shortify(norml_data + alias_data))
        self.data.update(dict(norml_data + alias_data + short_data))
        # print(sorted(self.data.items()), ':vlp2')
        for k, v in self.data.items():
            self.insert(k, v)
    
    @staticmethod
    def _resolve_references(data: t.Dict[str, t.Any]) -> T.Data:
        def get_real_value(key: str) -> t.Any:
            val = data[key]
            if isinstance(val, str) and val.startswith('$'):
                return get_real_value(val[1:])
            else:
                return val
            
        for k in data.keys():
            yield k, get_real_value(k)
    
    def _normalize(self, data: T.Data) -> T.Data:
        raise NotImplementedError
    
    def _create_similars(self, data: T.Data) -> T.Data:
        raise NotImplementedError
    
    def _shortify(self, data: T.Data) -> T.Data:
        raise NotImplementedError
