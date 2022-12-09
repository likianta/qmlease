from __future__ import annotations

import typing as t

from qtpy.QtCore import QObject as QObjectBase
from qtpy.QtCore import Signal

from .property import AutoProp
from .signal_slot import slot

__all__ = ['QObject', 'QObjectBaseWrapper']


class DynamicSignalMeta(type(QObjectBase)):
    # https://stackoverflow.com/a/63411358/9695911
    
    def __new__(cls, name, bases, dict_):
        # print(':d', name)
        # print(name, bases, dict_, ':l')
        
        custom_props = []
        for k, v in tuple(dict_.items()):
            if isinstance(v, AutoProp):
                custom_props.append(k)
                print('auto create signal', k + '_changed')
                dict_[k] = v.default
                dict_[k + '_changed'] = Signal(v.type_)
        dict_['_custom_props'] = tuple(custom_props)
        
        # noinspection PyTypeChecker
        return super().__new__(cls, name, bases, dict_)


class QObject(QObjectBase, metaclass=DynamicSignalMeta):
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
                    console.log(my_obj.qget('width'))
                    my_obj.width_changed.connect(...)
                }
            }
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def __getitem__(self, item: str):
        return self.property(item)
    
    def __setitem__(self, key: str, value: t.Any):
        self.setProperty(key, value)
    
    def __getattr__(self, item) -> t.Any:
        return super().__getattribute__(item)
    
    def __setattr__(self, key, value) -> None:
        # if isinstance(key, str) and key in getattr(self, '_custom_props', ()):
        if isinstance(key, str) and key in self._custom_props:
            if getattr(self, key) != value:
                super().__setattr__(key, value)
                getattr(self, key + '_changed').emit(value)
                return
        super().__setattr__(key, value)
    
    @slot(str, result=object)
    def qget(self, name: str) -> t.Any:
        return getattr(self, name)
    
    @slot(str, object)
    def qset(self, name: str, value: t.Any) -> None:
        setattr(self, name, value)


def enhance_origin_qobj(qobj: QObjectBase) -> QObject:  # DELETE
    def getitem(self, item: str):
        return self.property(item)
    
    def setitem(self, key: str, value: t.Any):
        self.setProperty(key, value)
    
    setattr(qobj, '__QObject_getitem__', getitem)
    setattr(qobj, '__QObject_setitem__', setitem)
    
    return qobj


class QObjectBaseWrapper:
    """
    a wrapper for QObjectBase, to enhance it's features.
    see also `.signal_slot : def slot : decorator : func_wrapper`.
    """
    
    def __init__(self, qobj: QObjectBase):
        """
        if you have only QObjectBase instance, you can pass it here to get the
        similar features like `QObject`.
        """
        self.qobj = qobj
    
    def __getattr__(self, item):
        if isinstance(item, str):
            if item.endswith('_changed'):
                return getattr(self.qobj, item.replace('_changed', 'Changed'))
            elif item != 'qobj' and item != 'children':
                return getattr(_getattr(self, 'qobj'), item)
        return _getattr(self, item)
    
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
    
    def children(self) -> list[QObjectBaseWrapper]:
        out = []
        for i in QObjectBase.children(self.qobj):
            if i.property('enabled') is None:
                # a weird item, it is invisible and unreasonable to exist.
                continue
            out.append(QObjectBaseWrapper(i))
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
    return QObjectBase.__getattribute__(self, key)


def _qsetattr(self, key, value) -> None:
    QObjectBase.__setattr__(self, key, value)
