from __future__ import annotations

import typing as t

from .model import Model
from ...qtcore import Slot


class T:
    Datum = t.Any
    Data = t.Iterable[Datum]


class SimpleModel(Model):
    
    def __init__(self, data: t.Iterable[t.Any] = ()):
        super().__init__(role_names=('value',))
        # self._data = list(data)
        if data:
            self._items = [{'value': x} for x in data]
    
    def __getitem__(self, item: int) -> T.Datum:
        return self._items[item]['value']
    
    def __setitem__(self, key: int, value: T.Datum) -> None:
        super().update(key, {'value': value})
    
    def __iter__(self):
        return (x['value'] for x in self._items)
    
    @Slot('any')
    def append(self, item: T.Datum) -> None:
        super().append({'value': item})
    
    @Slot(list)
    def append_many(self, items: T.Data) -> None:
        super().append_many([{'value': x} for x in items])
    
    extend = append_many
    
    @Slot(int, 'any')
    def insert(self, index: int, item: T.Datum) -> None:
        super().insert(index, {'value': item})
    
    @Slot(int, list)
    def insert_many(self, index: int, items: T.Data) -> None:
        super().insert_many(index, [{'value': x} for x in items])
    
    @Slot(result=...)
    def pop(self) -> T.Datum:
        return super().pop()['value']
    
    @Slot(int, result=list)
    def pop_many(self, count: int) -> T.Data:
        return [x['value'] for x in super().pop_many(count)]
    
    @Slot(int, result=...)
    def delete(self, index: int) -> T.Datum:
        return super().delete(index)['value']
    
    @Slot(int, int, result=list)
    def delete_many(self, index: int, count: int) -> T.Data:
        return [x['value'] for x in super().delete_many(index, count)]
    
    @Slot(int, result=...)
    def get(self, index: int) -> T.Datum:
        return super().get(index)['value']
    
    @Slot(int, result=list)
    @Slot(int, int, result=list)
    def get_many(
            self,
            start: int = None,
            end: int = None,
    ) -> T.Data:
        return [x['value'] for x in super().get_many(start, end)]
    
    @Slot(int, 'any')
    def update(self, index: int, item: T.Datum) -> None:
        super().update(index, {'value': item})
    
    @Slot(int, list)
    def update_many(self, index: int, items: T.Data) -> None:
        super().update_many(index, [{'value': x} for x in items])
