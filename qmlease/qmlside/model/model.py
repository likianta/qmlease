import typing as t

from qtpy.QtCore import QAbstractListModel
from qtpy.QtCore import QModelIndex

from ...qtcore import Slot


class T:  # 'TypeHint'
    Defaults = t.Dict[str, t.Any]
    Item = t.Dict[str, t.Any]
    Items = t.List[Item]
    Schema = t.Tuple[str, ...]


class Model(QAbstractListModel):
    """
    references:
        https://pyblish.gitbooks.io/developer-guide/content/qml_and_python_interoperability.html
        https://stackoverflow.com/questions/54687953/declaring-a-qabstractlistmodel-as-a-property-in-pyside2
    """
    autocomplete: bool
    _defaults: T.Defaults  # see also `self._auto_complete`
    _items: T.Items
    _schema: T.Schema
    
    @classmethod
    def from_list(cls, xlist: T.Items) -> 'Model':
        instance = cls(xlist[0].keys())
        instance.append_many(xlist)
        return instance
    
    def __init__(
        self,
        roles: t.Union[t.Dict[str, t.Any], t.Iterable[str]],
        autocomplete: bool = True
    ) -> None:
        super().__init__()
        self.autocomplete = autocomplete
        self._schema = tuple(roles)
        self._items = []
        self._defaults = roles if isinstance(roles, dict) else {
            x: '' for x in roles
            #   trick: set default value to '' instead of None to improve
            #   compatibility.
        }
    
    # @property
    # def role_names(self):
    #     return self._schema
    
    @property
    def items(self) -> T.Items:
        return self._items
    
    def __len__(self):
        return len(self._items)
    
    def __bool__(self):
        return bool(self._items)
    
    def __getitem__(self, index: int) -> dict:
        return self._items[index]
    
    def __iter__(self) -> t.Iterator[T.Item]:
        return iter(self._items)
    
    # -------------------------------------------------------------------------
    # api
    # tip: all params which named `item` or `items` accept partial dict.
    
    @Slot(dict)
    def append(self, item: T.Item) -> None:
        self.beginInsertRows(
            QModelIndex(), self.rowCount(), self.rowCount()
        )
        self._items.append(self._auto_complete(item))
        self.endInsertRows()
    
    @Slot(list)
    def append_many(self, items: T.Items) -> None:
        self.beginInsertRows(
            QModelIndex(), self.rowCount(), self.rowCount() + len(items) - 1
        )
        self._items.extend(map(self._auto_complete, items))
        self.endInsertRows()
    
    @Slot(int, dict)
    def insert(self, index: int, item: T.Item) -> None:
        self.beginInsertRows(
            QModelIndex(), index, index
        )
        self._items.insert(index, self._auto_complete(item))
        self.endInsertRows()
    
    @Slot(int, list)
    def insert_many(self, index: int, items: T.Items) -> None:
        self.beginInsertRows(
            QModelIndex(), index, index + len(items) - 1
        )
        self._items[index:index] = list(map(self._auto_complete, items))
        self.endInsertRows()
    
    @Slot(result=dict)
    def pop(self) -> T.Item:
        self.beginRemoveRows(
            QModelIndex(), len(self._items) - 1, len(self._items) - 1
        )
        out = self._items.pop(0)
        self.endRemoveRows()
        return out
    
    @Slot(int, result=list)
    def pop_many(self, count: int) -> T.Items:
        assert count > 0
        self.beginRemoveRows(
            QModelIndex(), len(self._items) - count, len(self._items) - 1
        )
        a, b = self._items[:-count], self._items[-count:]
        self._items = a
        self.endRemoveRows()
        return b
    
    @Slot(int, result=dict)
    def delete(self, index: int) -> T.Item:
        self.beginRemoveRows(
            QModelIndex(), index, index
        )
        out = self._items.pop(index)
        self.endRemoveRows()
        return out
    
    @Slot(int, int, result=list)
    def delete_many(self, index: int, count: int) -> T.Items:
        assert count > 0
        self.beginRemoveRows(
            QModelIndex(), index, index + count - 1
        )
        a, b = (self._items[:index] + self._items[index + count:],
                self._items[index:index + count])
        self._items = a
        self.endRemoveRows()
        return b
    
    @Slot(int, int)
    def move(self, old_index: int, new_index: int) -> None:
        self.beginMoveRows(
            QModelIndex(), old_index, old_index, QModelIndex(), new_index
        )
        item = self._items.pop(old_index)
        self._items.insert(new_index, item)
        self.endMoveRows()
    
    @Slot(int, int, int)
    def move_many(self, old_index: int, new_index: int, count: int) -> None:
        assert count > 0
        self.beginMoveRows(
            QModelIndex(), old_index, old_index + count - 1,
            QModelIndex(), new_index
        )
        items = self._items[old_index:old_index + count]
        self._items[old_index:old_index + count] = []
        self._items[new_index:new_index] = items
        self.endMoveRows()
    
    @Slot(int, result=bool)
    def move_up(self, index: int) -> bool:
        if index > 0:
            self.move(index, index - 1)
            return True
        return False
    
    @Slot(int, result=bool)
    def move_down(self, index: int) -> bool:
        if index < len(self._items) - 1:
            self.move(index, index + 1)
            return True
        return False
    
    @Slot()
    def clear(self) -> None:
        self.beginRemoveRows(
            QModelIndex(), 0, len(self._items) - 1
        )
        self._items.clear()
        self.endRemoveRows()
    
    @Slot(int, result=dict)
    def get(self, index: int) -> T.Item:
        return self._items[index]
    
    @Slot(int, result=list)
    @Slot(int, int, result=list)
    def get_many(
            self,
            start: int = None,
            end: int = None,  # TODO: shall we use `count` instead?
    ) -> T.Items:
        if start is not None and end is None:
            start, end = 0, start
        else:
            assert start is not None and end is not None
        return self._items[start:end]
    
    @Slot(int, dict)
    def update(self, index: int, item: dict) -> None:
        self._items[index].update(item)
        # emit signal of `self.dataChanged` to notify qml side that some item
        # has been changed.
        # `dataChanged.emit` accepts two arguments:
        #   dataChanged.emit(QModelIndex start, QModelIndex end)
        # how to create QModelIndex instance: use `self.createIndex(row, col)`.
        # ref: https://blog.csdn.net/LaoYuanPython/article/details/102011031
        qindex = self.createIndex(index, 0)
        self.dataChanged.emit(  # noqa
            qindex, qindex, [self._schema.index(x) for x in item.keys()]
        )
    
    @Slot(int, list)
    def update_many(self, start: int, items: T.Items) -> None:
        if not items: return
        end = start + len(items)
        for old, new in zip(self._items[start:end], items):
            old.update(new)
        qindex_start = self.createIndex(start, 0)
        qindex_end = self.createIndex(end - 1, 0)
        self.dataChanged.emit(qindex_start, qindex_end)  # noqa
    
    def _auto_complete(self, item: dict) -> T.Item:
        if self.autocomplete:
            for k, v in self._defaults.items():
                if k not in item:
                    item[k] = v
        return item
    
    # -------------------------------------------------------------------------
    # overrides
    
    # noinspection PyMethodOverriding
    def data(self, index: QModelIndex, role: int):
        key = self._schema[role]
        return self._items[index.row()].get(key, '')
    
    # noinspection PyMethodOverriding,PyTypeChecker,PyUnresolvedReferences
    def setData(self, index, value, role):
        key = self._schema[role]
        self._items[index.row()][key] = value
        self.dataChanged.emit(index, index)
    
    def rowCount(self, parent=QModelIndex()):  # noqa
        return len(self._items)
    
    def roleNames(self) -> t.Dict[int, bytes]:
        return {i: k.encode('utf-8') for i, k in enumerate(self._schema)}
        # return dict(enumerate(self._schema))
