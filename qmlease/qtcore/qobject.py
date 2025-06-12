import typing as t
from functools import partial

from qtpy.QtCore import QObject as OriginQObject
from qtpy.QtCore import Signal

from .property import AutoProp
from .signal_slot import slot


class PartialDelegate:
    self_qobj: 'QObject'
    
    def get(self, key: str) -> t.Any:
        # print(self.self_qobj, key, ':v')
        return getattr(self.self_qobj, key)
    
    def set(self, key: str, value: t.Any) -> None:
        # print(self.self_qobj, key, value, ':v')
        setattr(self.self_qobj, key, value)


class DynamicPropMeta(type(OriginQObject)):
    # https://stackoverflow.com/a/63411358/9695911
    
    def __new__(cls, name, bases, dict_):
        custom_props = []
        delegate = PartialDelegate()
        
        for k, v in tuple(dict_.items()):
            if isinstance(v, AutoProp):
                custom_props.append(k)
                
                dict_[k] = v.default
                if v.notify:
                    # print('auto create signal', f'{k}_changed', ':v')
                    dict_[f'{k}_changed'] = Signal(v.type)
                
                # create slot functions for qml getter & setter
                assert f'get_{k}' not in dict_
                func = partial(delegate.get, key=k)
                dict_[f'get_{k}'] = func
                slot(name=f'get_{k}', result=v.type)(func)
                
                if not v.const:
                    assert f'set_{k}' not in dict_
                    func = partial(delegate.set, k)
                    #   do not use `key=k` here, see reason:
                    #       https://stackoverflow.com/questions/26182068
                    #       /typeerror-got-multiple-values-for-argument-after
                    #       -applying-functools-partial
                    dict_[f'set_{k}'] = func
                    slot(v.type, name=f'set_{k}')(func)
        
        dict_['_auto_prop_delegate'] = delegate
        dict_['_custom_props'] = tuple(custom_props)
        
        # noinspection PyTypeChecker
        return super().__new__(cls, name, bases, dict_)


class QObject(OriginQObject, metaclass=DynamicPropMeta):
    """
    features:
        alternative to `property` and `setProperty`:
            before:
                qobj.property('width')
                qobj.setProperty('width', 100)
            after:
                qobj['width']
                qobj['width'] = 100
            note: the `property` and `setProperty` are still available.
            
        eliminate IDE `UnresolvedReference` warning:
            qobj.textChanged.connect(...)
            #    ~~~~~~~~~~~ warning gone
            
        an enhanced `property`:
            class MyObj(QObject):
                width = AutoProp(100, int)
            my_obj = MyObj()
            my_obj.width  # got 100
            my_obj.width = 200  # changed to 200, and auto emit
            #   `my_obj.width_changed` signal.
            
            // also can be recognized in qml side
            Item {
                Component.onCompleted: {
                    console.log(my_obj.get_width())
                    my_obj.width_changed.connect(...)
                    my_obj.set_width(300)
                }
            }
    """
    
    def __init__(self, parent: OriginQObject = None) -> None:
        super().__init__(parent)
        self._auto_prop_delegate.self_qobj = self
    
    def __getitem__(self, item: str) -> t.Any:
        return self.property(item)
    
    def __setitem__(self, key: str, value: t.Any) -> None:
        self.setProperty(key, value)
    
    def __getattr__(self, item: str) -> t.Any:
        # behave as is. just eliminate IDE warning
        return super().__getattribute__(item)
    
    def __setattr__(self, key: str, value: t.Any) -> None:
        if isinstance(key, str) and key in getattr(self, '_custom_props', ()):
            if getattr(self, key) != value:
                super().__setattr__(key, value)
                getattr(self, f'{key}_changed').emit(value)
                return
        super().__setattr__(key, value)
    
    @property
    def qobj(self) -> t.Self:
        return self
    
    def children(self) -> t.List['QObject']:
        out = []
        for child in OriginQObject.children(self):
            if child.property('enabled') is None:
                # a weird item, it is invisible and unreasonable to exist.
                continue
            out.append(QObjectDelegate(child))
        return out
    
    def has_prop(self, key: str) -> bool:
        return self[key] is not None
    
    def get_auto_prop(self, key: str) -> t.Any:
        print(self, key, ':v')
        return getattr(self, key)
    
    def set_auto_prop(self, key: str, new: t.Any) -> None:
        setattr(self, key, new)
    
    @slot(str, result=object)
    def qget(self, name: str) -> t.Any:
        return getattr(self, name)
    
    @slot(str, object)
    def qset(self, name: str, value: t.Any) -> None:
        setattr(self, name, value)


class QObjectDelegate:
    
    def __init__(self, qobj: OriginQObject):
        self.qobj = qobj
    
    def __getattr__(self, item: str):
        if item == 'qobj' or item == 'children':
            return _getattr(self, item)
        else:
            return getattr(_getattr(self, 'qobj'), item)
    
    def __setattr__(self, key, value):
        if isinstance(key, str):
            if key != 'qobj':
                setattr(_getattr(self, 'qobj'), key, value)
                return
        _setattr(self, key, value)
    
    def __getitem__(self, item: str):
        return self.qobj.property(item)
    
    def __setitem__(self, key: str, value: t.Any):
        self.qobj.setProperty(key, value)
    
    def children(self) -> t.List['QObjectDelegate']:
        out = []
        for i in OriginQObject.children(self.qobj):
            if i.property('enabled') is None:
                # a weird item, it is invisible and unreasonable to exist.
                continue
            out.append(QObjectDelegate(i))
        return out


# -----------------------------------------------------------------------------
# magic methods

def _getattr(self, key) -> t.Any:
    """ the primitive `getattr` method. """
    return object.__getattribute__(self, key)


def _setattr(self, key, value) -> None:
    """ the primitive `setattr` method. """
    object.__setattr__(self, key, value)


def _qgetattr(self, key) -> t.Any:
    return OriginQObject.__getattribute__(self, key)


def _qsetattr(self, key, value) -> None:
    OriginQObject.__setattr__(self, key, value)
