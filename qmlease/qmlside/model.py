from qtpy.QtCore import QAbstractListModel
from qtpy.QtCore import QModelIndex

from ..qt_core import slot


class T:  # 'TypeHint'
    from typing import Any, Dict, Iterable, List
    
    Item = Dict[str, Any]
    Items = List[Item]
    
    RoleNames = Iterable[str]
    Role2Name = Dict[int, str]
    Name2Role = Dict[str, int]


class Model(QAbstractListModel):
    """
    references:
        https://pyblish.gitbooks.io/developer-guide/content/qml_and_python
            _interoperability.html
        https://stackoverflow.com/questions/54687953/declaring-a
            -qabstractlistmodel-as-a-property-in-pyside2
    """
    _role_2_name: T.Role2Name
    _name_2_role: T.Name2Role
    _items: T.Items
    
    def __init__(self, role_names: T.RoleNames):
        super().__init__(None)
        self._name_2_role = {x: i for i, x in enumerate(role_names)}
        self._role_2_name = {v: k for k, v in self._name_2_role.items()}
        self._items = []
    
    @property
    def role_names(self):
        return tuple(self._name_2_role.keys())
    
    @property
    def items(self) -> T.Items:
        return self._items
    
    def __len__(self):
        return len(self._items)
    
    def __bool__(self):
        return bool(self._items)
    
    def __getitem__(self, index: int) -> dict:
        return self._items[index]
    
    # -------------------------------------------------------------------------
    # pyside api
    # tip: all params which named `item` or `items` accept partial dict.
    
    def append(self, item: T.Item):
        self.beginInsertRows(
            QModelIndex(), self.rowCount(), self.rowCount()
        )
        self._items.append(self._fill_item(item))
        self.endInsertRows()
    
    def append_many(self, items: T.Items):
        self.beginInsertRows(
            QModelIndex(), self.rowCount(), self.rowCount() + len(items) - 1
        )
        self._items.extend(map(self._fill_item, items))
        self.endInsertRows()
    
    def insert(self, index: int, item: T.Item):
        self.beginInsertRows(
            QModelIndex(), index, index
        )
        self._items.insert(index, self._fill_item(item))
        self.endInsertRows()
    
    def insert_many(self, index: int, items: T.Items):
        self.beginInsertRows(
            QModelIndex(), index, index + len(items) - 1
        )
        self._items[index:index] = list(map(self._fill_item, items))
        self.endInsertRows()
    
    def pop(self):
        self.beginRemoveRows(
            QModelIndex(), len(self._items) - 1, len(self._items) - 1
        )
        self._items.pop(0)
        self.endRemoveRows()
    
    def pop_many(self, count: int):
        assert count > 0
        self.beginRemoveRows(
            QModelIndex(), len(self._items) - count, len(self._items) - 1
        )
        self._items = self._items[:-count]
        self.endRemoveRows()
    
    def delete(self, index: int):
        self.beginRemoveRows(
            QModelIndex(), index, index
        )
        self._items.pop(index)
        self.endRemoveRows()
    
    def delete_many(self, index: int, count: int):
        assert count > 0
        self.beginRemoveRows(
            QModelIndex(), index, index + count - 1
        )
        self._items = self._items[:index] + self._items[index + count:]
        self.endRemoveRows()
    
    def clear(self):
        self.beginRemoveRows(
            QModelIndex(), 0, len(self._items) - 1
        )
        self._items.clear()
        self.endRemoveRows()
    
    def get(self, index: int) -> T.Item:
        return self._items[index]
    
    def get_many(self, start: int, end: int) -> T.Items:
        return self._items[start:end]
    
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
            qindex, qindex, [self._name_2_role[x] for x in item.keys()]
        )
    
    def update_many(self, start: int, end: int, items: T.Items) -> None:
        assert len(items) == end - start >= 0
        if end == start: return
        for old, new in zip(self._items[start:end], items):
            old.update(new)
        qindex_start = self.createIndex(start, 0)
        qindex_end = self.createIndex(end - 1, 0)
        self.dataChanged.emit(qindex_start, qindex_end)  # noqa
    
    set = update
    set_many = update_many
    
    def _fill_item(self, item: dict) -> T.Item:
        for k in self._name_2_role:
            if k not in item:
                item[k] = None  # FIXME: alternate: `item[k] = ''`
        return item
    
    # -------------------------------------------------------------------------
    # qml side api
    
    @slot(dict)
    def qappend(self, item: dict):
        self.append(item)
    
    @slot(int, result=dict)
    def qget(self, index: int):
        return self.get(index)
    
    @slot(int, dict)
    def qupdate(self, index: int, item: dict):
        self.update(index, item)
    
    # -------------------------------------------------------------------------
    # overrides
    
    # noinspection PyMethodOverriding
    def data(self, index, role: int):
        name = self._role_2_name[role]
        return self._items[index.row()].get(name, '')
    
    # noinspection PyMethodOverriding,PyTypeChecker,PyUnresolvedReferences
    def setData(self, index, value, role):
        name = self.role_names[role]
        self._items[index.row()][name] = value
        self.dataChanged.emit(index, index)
    
    def rowCount(self, parent=QModelIndex()):  # noqa
        return len(self._items)
    
    def roleNames(self) -> T.Dict[int, bytes]:
        # return self._role_2_name
        return {k: v.encode('utf-8') for k, v in self._role_2_name.items()}
