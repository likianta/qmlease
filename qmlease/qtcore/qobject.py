from __future__ import annotations

import typing as t

from qtpy.QtCore import QObject as QObjectBase

from .property import Property


class QObject(QObjectBase):
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
                width = Property(100, int)
            my_obj = MyObj()
            my_obj.width  # got 100
            my_obj.width = 200  # changed to 200, and auto emit
            #   `my_obj.width_changed` signal.
            
            // also can be recognized in qml side
            Item {
                width: my_obj.width  // got 100
                // when pyside has changed the value, qml will be notified, too.
            }
    """
    
    def __init__(self, parent=None):
        custom_props = []
        for k, v in self.__dict__.items():
            if isinstance(v, Property):
                custom_props.append(k)
                setattr(self, k, v)
                setattr(self, k + '_changed', v.value_changed)
        self._custom_props = tuple(custom_props)
        super().__init__(parent)
    
    def __getitem__(self, item: str):
        return self.property(item)
    
    def __setitem__(self, key: str, value: t.Any):
        self.setProperty(key, value)
    
    def __getattr__(self, item) -> t.Any:
        if isinstance(item, Property):
            return item.get_value()
        return super().__getattribute__(item)
    
    def __setattr__(self, key, value) -> None:
        if key in self._custom_props:
            getattr(self, key).set_value(value)
            return
        super().__setattr__(key, value)


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
            if item != 'qobj' and item != 'children':
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

def _getattr(self, key) -> t.Any:
    """ the primitive `getattr` method. """
    return object.__getattribute__(self, key)


def _setattr(self, key, value) -> None:
    """ the primitive `setattr` method. """
    object.__setattr__(self, key, value)
