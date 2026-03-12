import typing as t
from .signal import Signal

_get_type_of = type

class Property:
    """
    this is a dataclass-like class, just stores some info for laterly used by -
    `.qobject.DynamicPropMeta.__new__`.
    
    usage:
        class MyObject(QObject):
            # this derives four attributes:
            #   index: int
            #   _qget_index() -> int
            #   _qset_index(value: int) -> None
            #   index_changed: Signal[int]
            index = Property(0)
            
            def test(self):
                # get value
                print(self.index)  # -> 0
                print(self.get_index())  # -> 0
                print(type(self.index))  # -> int
                
                # set value
                self.index = 1  # -> 1
                self.index += 1  # -> 2
                self.set_index(3)  # -> 3
                
                # bind signal
                @self.index_changed.connect
                def _(value: int) -> None:
                    print(value)
    """
    default: t.Any
    notify: t.Union[bool, Signal]
    readonly: int  # DELETE?
    #   0: can be modified
    #   1: can be modified in python side, forbidden in qml side.
    #   2: forbidden modification in both python side and qml side.
    type: t.Type
    
    def __init__(
        self,
        value: t.Any,
        type: t.Type = None,
        notify: t.Union[bool, Signal] = True,
    ) -> None:
        """
        params:
            notify:
                if true, when value changed, it will emit `value_changed` 
                signal. this signal is auto created in stage of
                `.qobject.DynamicSignalMeta.__new__`.

                if false, it means this property is "readonly". if caller tries
                to set it, it will raise an exception.

                if given a custom signal, in the qml side, this property is 
                "readonly" (like `notify=False` does), but python side can 
                modify it freely.
                it means the property value may be varied between qml and python 
                side, unless the custom signal is emitted once.
                this is seldomly used case. you can see only usage at 
                `../style/color.py`.
        """
        assert isinstance(notify, (bool, Signal))
        self.default = value
        self.type = type or _get_type_of(value)
        self.notify = notify
        self.readonly = 0 if notify is True else 2 if notify is False else 1

# -----------------------------------------------------------------------------
# DELETE

'''
class ValueHolder(QObject):  # TEST
    
    def __init__(self, value: t.Any, final_type: type):
        super().__init__()
        self._value = value
        self.value_changed = signal(final_type)
        # self._notifier = notifier
        # self.value_changed = notifier
    
    def get_value(self):
        return self._value
    
    def set_value(self, new: t.Any) -> None:
        if self._value != new:
            self._value = new
    
    # @property
    # def value_changed(self) -> signal | None:
    #     return self._notifier


class Property(PropertyBase):
    """
    see feature introduction in `.qobject.QObject : class-level docstring`.
    """
    type_: type
    _core: QObject
    _value: t.Any
    value_changed: t.Optional[signal]
    
    def __init__(self, value: t.Any, *types: t.Union[t.Type, str]):
        assert 0 <= len(types) <= 3
        #   possible types:
        #       ()  # nothing. it is same with `('auto',)`
        #       (int, )  # or str, bool, float, ...
        #       (int, 'const')
        #       (int, 'final')
        #       (int, 'const', 'final')
        #       ('auto', )
        #       ('auto', 'const')
        #       ('auto', 'final')
        #       ('auto', 'const', 'final')
        
        self._value = value
        
        auto = 'auto' in types if types else True
        const = 'const' in types
        final = 'final' in types
        if auto:
            final_type = self._auto_detect_type(value)
        else:
            # assert len(types) > 0
            assert types[0] in (bool, float, int, str)
            final_type = types[0]
        self.type_ = final_type
        
        # if not const and not final:
        #     self.value_changed = signal(final_type)
        # else:
        #     self.value_changed = None
        if not const and not final:
            self.value_changed = SignalInstance()
            self.value_changed = ValueHolder(value, final_type).value_changed
        else:
            self.value_changed = None
        
        # noinspection PyTypeChecker
        super().__init__(
            final_type,
            self.get_value,
            self.set_value,
            # notify=self.value_changed,
            constant=const, final=final,
        )
        
        # value_holder = ValueHolder(value, (
        #     signal(final_type) if (not const and not final) else None
        # ))
        # super().__init__(
        #     final_type,
        #     value_holder.get_value,
        #     value_holder.set_value,
        #     notify=value_holder.value_changed,
        #     constant=const, final=final,
        # )
    
    def set_core(self, qobj: QObject) -> None:
        self._core = qobj
    
    def get_value(self) -> t.Any:
        return self._value
    
    def set_value(self, new: t.Any, xxx) -> None:
        print('part 1', new, ':vs')
        print('part 2', xxx, ':vs')
        if self._value != new:
            self._value = new
            if self.value_changed:
                self.value_changed.emit(new)
    
    @staticmethod
    def _auto_detect_type(value: t.Any) -> t.Type:
        """
        support only basic types.
        """
        out = _get_type(value)
        assert out in (bool, float, int, str)
        return out
'''
