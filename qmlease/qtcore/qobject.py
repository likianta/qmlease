import typing as t
from functools import partial
from uuid import uuid1

from qtpy.QtCore import Property as QtProperty
from qtpy.QtCore import QObject as QtObject
from qtpy.QtCore import Signal as QtSignal
from qtpy.QtQml import QJSValue

from .property import Property
from .slot import Slot
from .. import _env


class PartialDelegate:
    _core: 'QObject'

    def post_init(self, qobj: 'QObject') -> None:
        self._core = qobj
    
    def default_qget(self, key, _) -> t.Any:
        # print(self._core, key, ':v')
        return getattr(self._core, f'_qprop_{key}')
    
    def default_qset(self, key: str, value: t.Any) -> None:
        # print(self._core, key, value, ':v')
        if getattr(self._core, f'_qprop_{key}') == value:
            return
        setattr(self._core, f'_qprop_{key}', value)
        getattr(self._core, f'{key}_changed').emit(value)


class DynamicPropMeta(type(QtObject)):
    # https://stackoverflow.com/a/63411358/9695911
    
    def __new__(cls, name, bases, attrs):
        custom_props = []
        delegate = PartialDelegate()
        
        if '__qinit__' in attrs:
            attrs['__qinit__'](attrs)
        
        for k, v in tuple(attrs.items()):
            if isinstance(v, Property):
                assert k[0] != '_', ('property name must not start with `_`', k)
                custom_props.append(k)
                
                # attrs[k] = v.default
                # attrs[f'_qget_{k}'] = partial(delegate.get, k)
                # # Slot(name=f'_qget_{k}', result=v.type)(func)
                # if v.notify is True:
                #     # print('auto create signal', f'{k}_changed', ':v')
                #     attrs[f'{k}_changed'] = QtSignal(v.type)
                #     if f'_qset_{k}' in attrs:
                #         pass  # this means user has overwritten the setter func.
                #     else:
                #         attrs[f'_qset_{k}'] = partial(delegate.set, k)
                #     #   the second argument can not be written as `key=k`, see 
                #     #   reason: https://stackoverflow.com/questions/26182068/typeerror-got-multiple-values-for-argument-after-applying-functools-partial
                #     # Slot(name=f'_qset_{k}', result=None)(func)
                
                attrs[f'_qprop_{k}'] = v.default
                if v.notify is True:
                    attrs[f'{k}_changed'] = QtSignal(v.type)
                    attrs[k] = QtProperty(
                        v.type, 
                        fget=attrs.get(
                            f'_qget_{k}', 
                            partial(delegate.default_qget, k)
                        ),
                        fset=attrs.get(
                            f'_qset_{k}', 
                            partial(delegate.default_qset, k)
                            #   the second argument can not be written as 
                            #   `key=k`, see reason: 
                            #   https://stackoverflow.com/questions/26182068/typeerror-got-multiple-values-for-argument-after-applying-functools-partial
                        ),
                        notify=attrs[f'{k}_changed']
                    )
                elif v.notify is False:
                    attrs[f'{k}_changed'] = _InvalidSignal(k, error=True)
                    attrs[k] = QtProperty(
                        v.type, 
                        fget=attrs.get(
                            f'_qget_{k}', 
                            partial(delegate.default_qget, k)
                        ),
                        constant=True,
                    )
                else:
                    attrs[f'{k}_changed'] = _InvalidSignal(k, error=False)
                    attrs[k] = QtProperty(
                        v.type, 
                        fget=attrs.get(
                            f'_qget_{k}', 
                            partial(delegate.default_qget, k)
                        ),
                        notify=v.notify
                    )
        
        attrs['_auto_prop_delegate'] = delegate
        attrs['_custom_props'] = frozenset(custom_props)
        
        return super().__new__(cls, name, bases, attrs)


class _InvalidSignal:
    def __init__(self, name: str, error: bool) -> None:
        self._name = name
        self._error = error
        
    def connect(self, *_, **__) -> None:
        raise Exception('invalid signal', self._name)
        
    def emit(self, *_, **__) -> None:
        if self._error:
            raise Exception(
                'property "{}" has no "_changed" signal'.format(self._name)
            )


class QObject(QtObject, metaclass=DynamicPropMeta):
    """
    features:
        syntax sugar to simplify getting and setting properties:
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
                width = Property(100)
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
    
    def __init__(self, parent: QtObject = None) -> None:
        super().__init__(parent)
        self._auto_prop_delegate.post_init(self)
        self._broken = False
    
    def __getitem__(self, item: str) -> t.Any:
        x = self.property(item)
        if isinstance(x, QJSValue):
            return x.toVariant()
        else:
            return x
    
    def __setitem__(self, key: str, value: t.Any) -> None:
        if self._broken:
            return
        try:
            self.setProperty(key, value)
        except RuntimeError as e:
            if (
                _env.QT_DEBUG and
                'Internal C++ object' in str(e) and
                'already deleted' in str(e)
            ):
                print(':pv7', 'invalidate broken qobject')
                self._broken = True
            else:
                raise e
    
    def __getattr__(self, key: str) -> t.Any:
        if isinstance(key, str):
            if (
                key == '_custom_props' or
                key.startswith(('_qprop_', '_qget_', '_qset_'))
            ):
                return super().__getattribute__(key)
            elif key in getattr(self, '_custom_props', ()):
                return getattr(self, f'_qprop_{key}')
        return super().__getattribute__(key)
    
    def __setattr__(self, key: str, value: t.Any) -> None:
        if (
            isinstance(key, str) and
            key[0] != '_' and
            key in getattr(self, '_custom_props', ())
        ):
            internal_key = f'_qprop_{key}'
            if getattr(self, internal_key) != value:
                super().__setattr__(internal_key, value)
                getattr(self, f'{key}_changed').emit(value)
                return
        super().__setattr__(key, value)
    
    @property
    def class_name(self) -> str:
        return self.__class__.__name__
    
    @property
    def qobj(self) -> t.Self:
        return self
    
    def parent(self) -> 'QObject':
        return t.cast(QObject, QObjectDelegate(QtObject.parent(self)))
    
    def children(self) -> t.List['QObject']:
        out = []
        for child in QtObject.children(self):
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
    
    @Slot(str, result=object)
    def qget(self, name: str) -> t.Any:
        return getattr(self, name)
    
    @Slot(str, object)
    def qset(self, name: str, value: t.Any) -> None:
        setattr(self, name, value)


class QObjectDelegate:
    
    def __init__(self, qobj: QtObject) -> None:
        self.qobj = qobj

    def __contains__(self, item: str) -> bool:
        return self.qobj.property(item) is not None
    
    def __getattr__(self, item: str) -> t.Any:
        if item in ('qobj', 'parent', 'children', 'class_name'):
            return _getattr(self, item)
        else:
            return getattr(_getattr(self, 'qobj'), item)
    
    def __setattr__(self, key: str, value: t.Any) -> None:
        if isinstance(key, str):
            if key != 'qobj':
                setattr(_getattr(self, 'qobj'), key, value)
                return
        _setattr(self, key, value)
    
    def __getitem__(self, item: str) -> t.Any:
        if item == 'model':
            # https://chatgpt.com/share/69ba3d6d-8b3c-800a-baf0-467740a07afb
            if '_modelId' in self:
                uid = self.qobj.property('_modelId')
                return _model_vendors[uid]

        x = self.qobj.property(item)
        if x is None:
            # raise Exception(
            #     f'property "{item}" for `{self.class_name}` not found!'
            # )
            print(
                'property "{}" for `{}` not found!'
                .format(item, self.class_name), ':v6p'
            )
            return None
        elif isinstance(x, QJSValue):
            return x.toVariant()
        else:
            return x
    
    def __setitem__(self, key: str, value: t.Any) -> None:
        if key == 'model':
            # assert isinstance(value, ListModel)
            # from ..qmlside import ListModel
            # if isinstance(value, ListModel):
            if '_modelId' not in self:
                uid = uuid1().hex
                self.qobj.setProperty('_modelId', uid)
                _model_vendors[uid] = value
        self.qobj.setProperty(key, value)
    
    @property
    def class_name(self) -> str:
        # e.g. 'LKColumn_QMLTYPE_18' -> 'LKColumn'
        # noinspection PyTypeChecker
        return self.qobj.metaObject().className().split('_QMLTYPE_')[0]
    
    def parent(self) -> 'QObject':
        return t.cast(QObject, QObjectDelegate(self.qobj.parent()))
    
    def children(self) -> t.List['QObjectDelegate']:
        out = []
        if self.class_name == 'Repeater':
            for i in range(self.qobj.property('count')):
                # noinspection PyUnresolvedReferences
                out.append(QObjectDelegate(self.qobj.itemAt(i)))
        else:
            for i in QtObject.children(self.qobj):
                if i.property('enabled') is None:
                    # a weird item, it is invisible and unreasonable to exist.
                    continue
                out.append(QObjectDelegate(i))
        return out


# https://chatgpt.com/share/69ba3d6d-8b3c-800a-baf0-467740a07afb
_model_vendors = {}


# -----------------------------------------------------------------------------
# magic methods

def _getattr(self, key: str) -> t.Any:
    """ the primitive `getattr` method. """
    return object.__getattribute__(self, key)


def _setattr(self, key: str, value: t.Any) -> None:
    """ the primitive `setattr` method. """
    object.__setattr__(self, key, value)


def _qgetattr(self, key: str) -> t.Any:
    return QtObject.__getattribute__(self, key)


def _qsetattr(self, key: str, value: t.Any) -> None:
    QtObject.__setattr__(self, key, value)
