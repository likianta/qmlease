import typing as t

from lk_utils import loads
from qtpy.QtQml import QQmlPropertyMap


class Base(QQmlPropertyMap):
    data: dict
    
    def __init__(self):
        super().__init__()
        self.data = {}
    
    def __getitem__(self, item: str) -> t.Any:
        return self.data[item]
    
    def __setitem__(self, key: str, value: t.Any) -> None:
        self.data[key] = value
        self.insert(key, value)
    
    # -------------------------------------------------------------------------
    
    def update_from_file(self, file: str) -> None:
        self.update(loads(file))
    
    def update(self, data: dict) -> None:
        plain_data = self._resolve_references(data)
        norm__data = self._normalize(plain_data)
        alias_data = self._create_similars(norm__data)
        short_data = self._shortify({**norm__data, **alias_data})
        self.data.update({**norm__data, **alias_data, **short_data})
        for k, v in self.data.items():
            self.insert(k, v)
    
    @staticmethod
    def _resolve_references(data: dict) -> dict:
        resolved = set()
        
        def eval_reference(value: str) -> t.Any:
            # assert value.startswith('$')
            base_key = value[1:]
            base_value = data[base_key]
            if isinstance(base_value, str) and base_value.startswith('$'):
                final_value = eval_reference(base_value)
                data[base_key] = final_value
                resolved.add(base_key)
                return final_value
            else:
                resolved.add(base_key)
                return base_value
        
        for i, (k, v) in enumerate(tuple(data.items())):
            if k in resolved:
                continue
            if isinstance(v, str) and v.startswith('$'):
                try:
                    data[k] = eval_reference(v)
                except KeyError as e:
                    print(':v4',
                          'failed dynamically assign value to key. '
                          '(source key does not exist!) '
                          'index: {}, key: {}, value: {}'.format(i, k, v))
                    raise e
        
        return data
    
    def _normalize(self, data: dict) -> dict:
        raise NotImplementedError
    
    def _create_similars(self, data: dict) -> dict:
        raise NotImplementedError
    
    def _shortify(self, data: dict) -> dict:
        raise NotImplementedError
