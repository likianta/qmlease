import typing as t

from qtpy.QtCore import QAbstractListModel
from qtpy.QtCore import QModelIndex

from ..qtcore import slot


class T:  # 'TypeHint'
    Defaults = t.Dict[str, t.Any]
    Item = t.Dict[str, t.Any]
    Items = t.List[Item]
    Role2Name = t.Dict[int, str]
    Name2Role = t.Dict[str, int]
    RoleNames = t.Union[
        t.Dict[str, t.Any],  # suggested
        t.Tuple[str, ...],
        t.List[str]
    ]


class Model(QAbstractListModel):
    """
    references:
        https://pyblish.gitbooks.io/developer-guide/content/qml_and_python
            _interoperability.html
        https://stackoverflow.com/questions/54687953/declaring-a
            -qabstractlistmodel-as-a-property-in-pyside2
    """
    _defaults: T.Defaults  # see also `self._auto_complete`
    _items: T.Items
    _name_2_role: T.Name2Role
    _role_2_name: T.Role2Name
    
    def __init__(self, role_names: T.RoleNames):
        super().__init__(None)
        self._name_2_role = {x: i for i, x in enumerate(role_names)}
        self._role_2_name = {i: x for i, x in enumerate(role_names)}
        self._items = []
        if isinstance(role_names, dict):
            self._defaults = role_names
        else:
            self._defaults = {x: None for x in role_names}
            #   TODO: or `{x: '', ...}`?
    
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
    
    def __iter__(self) -> t.Iterator[T.Item]:
        return iter(self._items)
    
    # -------------------------------------------------------------------------
    # api
    # tip: all params which named `item` or `items` accept partial dict.
    
    @slot(dict)
    def append(self, item: T.Item) -> None:
        self.beginInsertRows(
            QModelIndex(), self.rowCount(), self.rowCount()
        )
        self._items.append(self._auto_complete(item))
        self.endInsertRows()
    
    @slot(list)
    def append_many(self, items: T.Items) -> None:
        self.beginInsertRows(
            QModelIndex(), self.rowCount(), self.rowCount() + len(items) - 1
        )
        self._items.extend(map(self._auto_complete, items))
        self.endInsertRows()
    
    @slot(int, dict)
    def insert(self, index: int, item: T.Item) -> None:
        self.beginInsertRows(
            QModelIndex(), index, index
        )
        self._items.insert(index, self._auto_complete(item))
        self.endInsertRows()
    
    @slot(int, list)
    def insert_many(self, index: int, items: T.Items) -> None:
        self.beginInsertRows(
            QModelIndex(), index, index + len(items) - 1
        )
        self._items[index:index] = list(map(self._auto_complete, items))
        self.endInsertRows()
    
    @slot(result=dict)
    def pop(self) -> T.Item:
        self.beginRemoveRows(
            QModelIndex(), len(self._items) - 1, len(self._items) - 1
        )
        out = self._items.pop(0)
        self.endRemoveRows()
        return out
    
    @slot(int, result=list)
    def pop_many(self, count: int) -> T.Items:
        assert count > 0
        self.beginRemoveRows(
            QModelIndex(), len(self._items) - count, len(self._items) - 1
        )
        a, b = self._items[:-count], self._items[-count:]
        self._items = a
        self.endRemoveRows()
        return b
    
    @slot(int, result=dict)
    def delete(self, index: int) -> T.Item:
        self.beginRemoveRows(
            QModelIndex(), index, index
        )
        out = self._items.pop(index)
        self.endRemoveRows()
        return out
    
    @slot(int, int, result=list)
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
    
    @slot(int, int)
    def move(self, old_index: int, new_index: int) -> None:
        self.beginMoveRows(
            QModelIndex(), old_index, old_index, QModelIndex(), new_index
        )
        item = self._items.pop(old_index)
        self._items.insert(new_index, item)
        self.endMoveRows()
    
    @slot(int, int, int)
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
    
    @slot(int, result=bool)
    def move_up(self, index: int) -> bool:
        if index > 0:
            self.move(index, index - 1)
            return True
        return False
    
    @slot(int, result=bool)
    def move_down(self, index: int) -> bool:
        if index < len(self._items) - 1:
            self.move(index, index + 1)
            return True
        return False
    
    @slot()
    def clear(self) -> None:
        self.beginRemoveRows(
            QModelIndex(), 0, len(self._items) - 1
        )
        self._items.clear()
        self.endRemoveRows()
    
    @slot(int, result=dict)
    def get(self, index: int) -> T.Item:
        return self._items[index]
    
    @slot(int, result=list)
    @slot(int, int, result=list)
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
    
    @slot(int, dict)
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
    
    @slot(int, list)
    def update_many(self, start: int, items: T.Items) -> None:
        if not items: return
        end = start + len(items)
        for old, new in zip(self._items[start:end], items):
            old.update(new)
        qindex_start = self.createIndex(start, 0)
        qindex_end = self.createIndex(end - 1, 0)
        self.dataChanged.emit(qindex_start, qindex_end)  # noqa
    
    def _auto_complete(self, item: dict) -> T.Item:
        for k, v in self._defaults.items():
            if k not in item:
                item[k] = v
        return item
    
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
    
    def roleNames(self) -> t.Dict[int, bytes]:
        # return self._role_2_name
        return {k: v.encode('utf-8') for k, v in self._role_2_name.items()}
