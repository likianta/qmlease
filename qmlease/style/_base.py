import typing as t

from lk_utils import loads
from qtpy.QtQml import QQmlPropertyMap


class Base(QQmlPropertyMap):
    """
    once user is given a stylesheet file (like ".yaml"), this class should
    parse it and generate a finite set of extended stylesheets, which includes
    not only the original one, but also its variants.
    
    for example, if user stylesheet is:
        button_bg: '#ff0000'
        button_bg_pressed: '#00ff00'
    this class should generate:
        button_bg: '#ff0000'
        button_bg_pressed: '#00ff00'
        button_bg_focused: '#00ff00'
        button_bg_hovered: '#ff0000'  # based on some internal rules to pick
        #   the most familiar color.
        ...
    see also `self._post_complete()`
    """
    data: dict
    
    def __init__(self):
        super().__init__()
        self.data = {}
        
    def __getitem__(self, item: str) -> t.Any:
        return self.data[item]
    
    def __setitem__(self, key: str, value: t.Any) -> None:
        self.data[key] = value
        self.insert(key, value)
    
    def update_from_file(self, file: str) -> None:
        data: dict = loads(file)
        self.update(data)
    
    def update(self, data: dict) -> None:
        
        def eval_reference(value: str) -> t.Any:
            # assert value.startswith('$')
            base_key = value[1:]
            base_value = data[base_key]
            if isinstance(base_value, str) and base_value.startswith('$'):
                out = eval_reference(base_value)
                data[base_key] = out
                return out
            else:
                return base_value
        
        for i, (k, v) in enumerate(data.items()):
            if isinstance(v, str) and v.startswith('$'):
                try:
                    data[k] = eval_reference(v)
                except KeyError as e:
                    print(':v4',
                          'failed dynamically assign value to key. '
                          '(source key does not exist!) '
                          'index: {}, key: {}, value: {}'.format(i, k, v))
                    raise e
        
        data = self._post_complete(data)
        self._finalize(data)
    
    def _post_complete(self, data: dict) -> dict:
        raise NotImplementedError
    
    def _finalize(self, kwargs: dict) -> None:
        # https://stackoverflow.com/questions/62629628/attaching-qt-property-to
        # -python-class-after-definition-not-accessible-from-qml
        for k, v in kwargs.items():
            self[k] = v
