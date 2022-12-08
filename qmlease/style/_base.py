import typing as t

from lk_utils import loads


class Base:
    data: dict
    
    def __init__(self):
        self.data = {}
    
    def __getitem__(self, item: str) -> t.Any:
        # return self.get(item)
        if item in self.data:
            return self.data[item]
        if similar := self._guess(item):
            self.data[item] = similar
            return similar
        return None
    
    def __setitem__(self, key: str, value: t.Any) -> None:
        self.data[key] = value
    
    def _guess(self, key: str) -> t.Any:
        raise NotImplementedError
    
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
        
        self.data.update({self.normalize(k): v for k, v in data.items()})
    
    def normalize(self, key: str) -> str:
        raise NotImplementedError
