from typing import Iterator
from qtpy.QtQml import QQmlPropertyMap


class Base(QQmlPropertyMap):
    
    def __init__(self):
        super().__init__()
    
    def update(self, data: dict):
        
        def _get_dynamic_value(value: str):  # -> Any
            # assert value.startswith('$')
            base_key = value[1:]
            base_value = data[base_key]
            if isinstance(base_value, str) and base_value.startswith('$'):
                out = _get_dynamic_value(base_value)
                data[base_key] = out
                return out
            else:
                return base_value
        
        for i, (k, v) in enumerate(data.items()):
            if isinstance(v, str) and v.startswith('$'):
                try:
                    data[k] = _get_dynamic_value(v)
                except KeyError as e:
                    print(':v4',
                          'Failed dynamically assign value to key'
                          '(source key does not exist)! '
                          'index: {}, key: {}, value: {}'.format(i, k, v))
                    raise e
        
        self._update(data)
    
    def update_from_file(self, file: str):
        from lk_utils import loads
        data: dict = loads(file)
        self.update(data)
    
    def _update(self, kwargs: dict):
        # https://stackoverflow.com/questions/62629628/attaching-qt-property-to
        # -python-class-after-definition-not-accessible-from-qml
        for k, v in kwargs.items():
            setattr(self, k, v)
            self.insert(k, v)
            for k_abbr in self._get_abbrs(k):
                self.insert(k_abbr, v)
    
    def _get_abbrs(self, name: str) -> Iterator[str]:
        raise NotImplementedError
