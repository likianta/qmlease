import re
import typing as t

from qtpy.QtCore import QObject
from qtpy.QtQml import QQmlContext
from qtpy.QtQml import QQmlPropertyMap
from qtpy.QtQml import qmlRegisterType

from .._env import QT_VERSION

if QT_VERSION >= 6.3:
    # https://www.qt.io/blog/qt-for-python-details-on-the-new-6.3-release
    from qtpy.QtQml import QmlNamedElement
elif QT_VERSION >= 6.0:
    from qtpy.QtQml import QmlElement
else:
    QmlNamedElement = None
    QmlElement = None


class Register:
    _namespace: 'Namespace'
    _root: QQmlContext
    # the holder is made for preventing the objects which were registered to
    #   qml side from being recycled by python garbage collector incorrectly.
    __hidden_ref: t.Dict[int, QObject]
    
    def __init__(self, root_context: QQmlContext):
        self._namespace = Namespace()
        self._root = root_context
        self.__hidden_ref = {}
        self._root.setContextProperty('py', self._namespace)
    
    def register(
        self,
        qobj: t.Union[QObject, type[QObject]],
        name: str = '',
        namespace: str = '',
    ) -> None:
        """
        register an instance or a subclass of QObject to qml side.
        
        detailed doc: docs/the-app-register-method.md

        args:
            qobj: either a QObject subclass or a subclass instance.
            name:
                what is it called in qml.
                if `qobj` is class type, suggest to use PascalCase.
                if `qobj` is instance, suggest to use snake_case or camelCase.
                if not given, will auto generate one based on its type and its
                class name.
                suggest: if you want to pass a custom name, it's better to use
                a fixed prefix, like 'Py'/'py', 'My'/'my', etc. for example
                'PyHotLoader', 'pylayout'.
                TODO: check conflicts with reserved names.
            namespace:
                style: if you are registering a class, use PascalCase;
                otherwise use snake_case.

        example:
            python side:
                from qmlease import app
                app.register(aaa, namespace='global')
                app.register(bbb, namespace='')
                app.register(ccc, namespace='my_space')
                app.register(DDD, namespace='global')
                app.register(EEE, namespace='')
                app.register(FFF, namespace='MyFirstApp')
            effects:
                `aaa` can be directly used as `aaa`.
                `bbb` can be used as `py.bbb`.
                `ccc` can be used as `py.my_first_app.ccc`.
                `DDD` will raise an error, because class type is not allowed to
                    be registered to global namespace.
                `EEE` will raise an error, because class type is not allowed to
                    be registered to anonymous namespace.
                `FFF` should be imported and be declared as `FFF {...}` to use.
            qml side:
                import QtQuick 2.15
                import MyFirstApp 1.0
                Item {
                    FFF { id: fff }
                    Component.onCompleted: {
                        console.log(aaa)
                        console.log(py.bbb)
                        console.log(py.my_space.ccc)
                        console.log(fff)
                    }
                }
        """
        # print(':v', name, qobj, isinstance(qobj, QObject))
        
        if isinstance(qobj, QObject):
            name = name or _pascal_2_snake_case(qobj.__class__.__name__)
            
            if namespace == '':
                self._namespace.insert(name, qobj)
            elif namespace == 'global':
                self._root.setContextProperty(name, qobj)
            else:
                print('register singleton instance "{}" to "{}"'
                      .format(name, namespace), ':vp')
                if not self._namespace.contains(namespace):
                    self._namespace.insert(namespace, Namespace())
                print(
                    (namespace, name),
                    self._namespace.contains(namespace),
                    self._namespace[namespace],
                    ':v'
                )
                self._namespace[namespace].insert(name, qobj)
                #: B
                # exec('QmlNamedElement(qname)(QmlSingleton(cls))', {
                #     'QML_IMPORT_NAME'         : namespace,
                #     'QML_IMPORT_MAJOR_VERSION': 1,
                #     'QML_IMPORT_MINOR_VERSION': 0,
                #     'QmlNamedElement'         : QmlNamedElement,
                #     'QmlSingleton'            : QmlSingleton,
                #     'qname'                   : name,
                #     'cls'                     : qcls,
                # })
                #: C
                # # noinspection PyTypeChecker
                # qmlRegisterSingletonInstance(
                #     qobj.__class__, namespace, 1, 0, name, qobj
                # )
        
        elif issubclass(qobj, QObject):
            name = name or qobj.__name__
            qcls = qobj
            
            if namespace == '':
                raise Exception(
                    'cannot register a class to anonymous namespace!'
                )
            elif namespace == 'global':
                raise Exception(
                    'cannot register a class to global namespace!'
                )
            else:
                print('register pytype class "{}" to "{}"'
                      .format(name, namespace), ':vp')
                if QmlNamedElement:
                    exec('QmlNamedElement(qname)(cls)', {
                        'QML_IMPORT_NAME'         : namespace,
                        'QML_IMPORT_MAJOR_VERSION': 1,
                        'QML_IMPORT_MINOR_VERSION': 0,
                        'QmlNamedElement'         : QmlNamedElement,
                        'qname'                   : name,
                        'cls'                     : qcls,
                    })
                elif QmlElement:  # TODO: not tested
                    qcls.__name__ = name
                    exec('QmlElement(cls)', {
                        'QML_IMPORT_NAME'         : namespace,
                        'QML_IMPORT_MAJOR_VERSION': 1,
                        'QML_IMPORT_MINOR_VERSION': 0,
                        'QmlElement'              : QmlElement,
                        'cls'                     : qcls,
                    })
                else:
                    # noinspection PyTypeChecker
                    qmlRegisterType(qcls, namespace, 1, 0, name)
        else:
            raise TypeError('target must be a QObject subclass or instance.')
        
        self.__hidden_ref[id(qobj)] = qobj
    
    def freeze(self) -> None:
        # self.__root.setContextProperty('py', self._namespace)
        pass
    
    def release(self) -> None:
        del self._namespace
        self._namespace = Namespace()
        self.__hidden_ref.clear()


class Namespace(QQmlPropertyMap):
    _subspaces: t.Dict[str, 'Namespace']  # patch for pyside6 v6.6+
    
    def __init__(self) -> None:
        super().__init__()
        self._subspaces = {}
    
    def __getitem__(self, sub_space_name: str) -> 'Namespace':
        return self._subspaces[sub_space_name]
    
    def insert(self, key, value) -> None:
        if isinstance(value, Namespace):
            self._subspaces[key] = value
        super().insert(key, value)


_name_pattern_1 = re.compile(r'(.)([A-Z][a-z]+)')
_name_pattern_2 = re.compile(r'([a-z0-9])([A-Z])')


def _pascal_2_snake_case(name: str) -> str:
    """
    https://stackoverflow.com/questions/1175208/

    examples:
        ClassicCase         -> classic_case
        camel2_camel2_case  -> camel2_camel2_case
        getHTTPResponseCode -> get_http_response_code
        HTTPResponseCodeXYZ -> http_response_code_xyz
    """
    name = _name_pattern_1.sub(r'\1_\2', name)
    return _name_pattern_2.sub(r'\1_\2', name).lower()
