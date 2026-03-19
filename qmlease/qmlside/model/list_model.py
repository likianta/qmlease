import typing as t
from lk_utils import textwrap as tw
from qtpy.QtCore import QAbstractListModel
from qtpy.QtCore import QModelIndex
from ...qtcore import Slot

class T:
    Defaults = t.Dict[str, t.Any]
    Item = t.Dict[str, t.Any]
    Items = t.List[Item]
    Roles = t.Union[t.Dict[str, t.Any], t.Iterable[str]]
    Schema = t.Tuple[str, ...]

class ListModel(QAbstractListModel):
    """
    references:
        https://pyblish.gitbooks.io/developer-guide/content/qml_and_python_interoperability.html
        https://stackoverflow.com/questions/54687953/declaring-a-qabstractlistmodel-as-a-property-in-pyside2
    """
    auto_complete: bool
    auto_submit: bool
    _defaults: T.Defaults  # see also `self._auto_complete`
    _items: T.Items
    _origin_list_length: int
    _schema: T.Schema
    _shadow_list: t.List[t.Optional[bool]]
    
    @classmethod
    def from_list(cls, xlist: T.Items, roles: T.Roles = None) -> 'ListModel':
        instance = cls(roles or xlist[0].keys(), auto_submit=False)
        instance.extend(xlist)
        instance.submit().always()
        return instance

    @classmethod
    def empty_copy(cls, instance: 'ListModel', **kwargs) -> 'ListModel':
        return cls(
            instance._schema, 
            auto_complete=kwargs.get('auto_complete', False), 
            auto_submit=kwargs.get('auto_submit', True),
        )
    
    def __init__(
        self,
        roles: T.Roles,
        auto_complete: bool = False,
        auto_submit: bool = True,
    ) -> None:
        super().__init__()
        self.auto_complete = auto_complete
        self.auto_submit = auto_submit
        self._schema = tuple(roles)
        self._items = []
        self._defaults = roles if isinstance(roles, dict) else {
            x: '' for x in roles
            #   trick: set default value to '' instead of None to improve
            #   compatibility.
        }
        self._shadow_list = []
        self._origin_list_length = 0
        # self._transactions = {
        #     '=': set(),
        #     '-': set(),
        #     '+': set(),
        # }
    
    @property
    def items(self) -> T.Items:
        return self._items
    
    def __bool__(self):
        return bool(self._items)
    
    def __getitem__(self, index: int) -> dict:
        return self._items[index]
    
    def __iter__(self) -> t.Iterator[T.Item]:
        return iter(self._items)
    
    def __len__(self):
        return len(self._items)
    
    def __str__(self) -> str:
        if self._items:
            return tw.wrap(
                '''
                <ListModel with {} items:
                    [
                        {}
                    ]
                >
                ''',
                lstrip=False,
            ).format(
                len(self._items),
                tw.join((
                    tw.wrap(
                        '''
                        {{
                            {}
                        }}
                        '''
                    ).format(
                        tw.join((
                            '"{}": {}'.format(
                                k, 
                                '"{}"'.format(v) if isinstance(v, str) else 
                                str(v).lstrip() if isinstance(v, ListModel) 
                                else v
                            )
                            for k, v in item.items()
                        ), 4, ',\n')
                    )
                    for item in self._items
                ), 8, ',\n')
            )
        else:
            return '<ListModel with 0 items>'
    
    # --------------------------------------------------------------------------

    @Slot(dict)
    def append(self, item: T.Item) -> None:
        index = len(self._items)
        if self.auto_submit:
            self.beginInsertRows(QModelIndex(), index, index)
            self._items.append(self._auto_complete(item))
            self.endInsertRows()
        else:
            self._items.append(self._auto_complete(item))
            self._shadow_list.append(True)
    
    @Slot(list)
    def extend(self, items: T.Items, *, index: int = -1) -> None:
        if index == -1:
            use_extend_method = True
            index = len(self._items)
        else:
            assert 0 <= index < len(self._items)

        if self.auto_submit:
            self.beginInsertRows(QModelIndex(), index, index + len(items) - 1)
            if use_extend_method:
                self._items.extend(map(self._auto_complete, items))
            else:
                self._items[index:index] = list(map(self._auto_complete, items))
            self.endInsertRows()
        else:
            if use_extend_method:
                self._items.extend(map(self._auto_complete, items))
                self._shadow_list.extend((True,) * len(items))
            else:
                self._items[index:index] = list(map(self._auto_complete, items))
                self._shadow_list[index:index] = [True] * len(items)
    
    @Slot(int, dict)
    def insert(self, index: int, item: T.Item) -> None:
        if self.auto_submit:
            self.beginInsertRows(QModelIndex(), index, index)
            self._items.insert(index, self._auto_complete(item))
            self.endInsertRows()
        else:
            self._items.insert(index, self._auto_complete(item))
            self._shadow_list.insert(index, True)
    
    @Slot(result=dict)
    @Slot(result=list)
    def pop(self, index: int = -1, *, count: int = 1) -> T.Item:
        pop_last = index == -1
        if index < 0:
            index = len(self._items) + index
        if count == 1:
            if self.auto_submit:
                self.beginRemoveRows(QModelIndex(), index, index)
                if pop_last:
                    out = self._items.pop()
                else:
                    out = self._items.pop(index)
                self.endRemoveRows()
            else:
                if pop_last:
                    out = self._items.pop()
                    self._shadow_list.pop()
                else:
                    out = self._items.pop(index)
                    self._shadow_list.pop(index)
        else:
            assert index + count <= len(self._items)
            out = self._items[index:index+count]
            if self.auto_submit:
                self.beginRemoveRows(QModelIndex(), index, index + count - 1)
                self._items[index:index+count] = []
                self.endRemoveRows()
            else:
                self._items[index:index+count] = []
                self._shadow_list[index:index+count] = []
        return out
    
    # extended method: move, move_up, move_down
    # these are convenience for user to drag and drop listview items.
    @Slot(int, int)
    def move(self, index_fo: int, index_to: int) -> None:
        if self.auto_submit:
            self.beginMoveRows(
                QModelIndex(), index_fo, index_fo, QModelIndex(), index_to
            )
            item = self._items.pop(index_fo)
            self._items.insert(index_to, item)
            self.endMoveRows()
        else:
            item = self._items.pop(index_fo)
            self._items.insert(index_to, item)
            self._shadow_list.pop(index_fo)
            self._shadow_list.insert(index_to, True)
    
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
        if self.auto_submit:
            self.beginRemoveRows(QModelIndex(), 0, len(self._items) - 1)
            self._items.clear()
            self.endRemoveRows()
        else:
            self._items.clear()
            self._shadow_list.clear()
    
    @Slot(int, result=dict)
    def get(self, index: int) -> T.Item:
        return self._items[index]
    
    def submit(self):
        assert len(self._shadow_list) == len(self._items)

        def aggregate_changes():
            if self._origin_list_length and self._shadow_list:
                temp = []
                for i in range(
                    min((self._origin_list_length, len(self._shadow_list)))
                ):
                    if self._shadow_list[i] is True:
                        temp.append(i)
                    else:
                        if temp:
                            yield ('update', temp[0], temp[-1])
                            temp.clear()
                if temp:
                    yield ('update', temp[0], temp[-1])

            if len(self._shadow_list) > self._origin_list_length:
                yield (
                    'insert', 
                    self._origin_list_length, 
                    len(self._shadow_list) - 1
                )
            elif len(self._shadow_list) < self._origin_list_length:
                yield (
                    'remove', 
                    len(self._shadow_list), 
                    self._origin_list_length - 1
                )
        
        for opt, start, end in aggregate_changes():
            match opt:
                case 'update':
                    self.dataChanged.emit(
                        self.createIndex(start, 0), self.createIndex(end, 0)
                    )
                case 'insert':
                    self.beginInsertRows(QModelIndex(), start, end)
                    self.endInsertRows()
                case 'remove':
                    self.beginRemoveRows(QModelIndex(), start, end)
                    self.endRemoveRows()
        self._shadow_list.clear()
        self._shadow_list.extend((None,) * len(self._items))
        self._origin_list_length = len(self._shadow_list)
        return self

    def always(self):
        """
        usage:
            my_list_model.submit().always()
        """
        self.auto_submit = True

    def _auto_complete(self, item: dict) -> T.Item:
        if self.auto_complete:
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
        self.dataChanged.emit(index, index, [role])
    
    def rowCount(self, parent=QModelIndex()):  # noqa
        return len(self._items)
    
    def roleNames(self) -> t.Dict[int, bytes]:
        return {i: k.encode('utf-8') for i, k in enumerate(self._schema)}
        # return dict(enumerate(self._schema))
