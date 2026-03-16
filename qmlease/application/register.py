import re
import typing as t

from qtpy.QtCore import QObject
from qtpy.QtQml import QQmlContext
from qtpy.QtQml import QQmlPropertyMap
# from qtpy.QtQml import qmlRegisterType

# from .._env import QT_VERSION
#
# if QT_VERSION >= (6, 3, 0):
#     # https://www.qt.io/blog/qt-for-python-details-on-the-new-6.3-release
#     from qtpy.QtQml import QmlNamedElement
# elif QT_VERSION >= (6, 0, 0):
#     from qtpy.QtQml import QmlElement
# else:
#     QmlNamedElement = None
#     QmlElement = None


class Register:
    _namespaces: t.Dict[str, 'Namespace']
    _root: QQmlContext
    # the holder is made for preventing the objects which were registered to
    #   qml side from being recycled by python garbage collector incorrectly.
    __hidden_ref: t.Dict[int, QObject]
    
    def __init__(self, root_context: QQmlContext):
        self._namespaces = {'py': Namespace()}
        self._root = root_context
        self.__hidden_ref = {}
        self._root.setContextProperty('py', self._namespaces['py'])
    
    def register(
        self,
        qobj: t.Union[QObject, type[QObject]],
        name: str = '',
        namespace: t.Union[t.Literal['global', 'py'], str] = 'py',
    ) -> None:
        """
        register an instance or a subclass of QObject to qml side.
        
        read in details: `docs/the-app-register-method.md`
        
        params:
            qobj: either a QObject subclass or a subclass instance.
            name:
                what is it called in qml. if not given, will auto generate one
                based on its class name. for example, `MyClass -> my_class`.
            namespace:
                preset namespaces:
                    '' or 'global':
                        register to global namespace.
                    'py':
                        register to `py` namespace.
                else (any other string):
                    register to the given namespace. be sure the custom 
                    namespace contains only `[a-zA-Z0-9_]`.

        example:
            python side:
                from qmlease import app
                app.register(aaa, namespace='py')
                app.register(bbb, namespace='global')
                app.register(ccc, namespace='')
                #   not suggested, use 'global' instead.
                app.register(ddd, namespace='myspace')
            results:
                `aaa` can be directly used as `py.aaa`.
                `bbb` can be used as `bbb`.
                `ccc` can be used as `ccc`.
                `ddd` can be used as `myspace.ddd`.
            qml side:
                import QtQuick
                Item {
                    EEE { id: eee }
                    Component.onCompleted: {
                        console.log(py.aaa)
                        console.log(bbb)
                        console.log(ccc)
                        console.log(myspace.ddd)
                        console.log(eee)
                    }
                }
        """
        # print(':v', name, qobj, type(qobj), isinstance(qobj, QObject))
        
        if isinstance(qobj, QObject):
            name = name or _pascal_2_snake_case(qobj.__class__.__name__)
            
            if namespace == 'py':
                self._namespaces['py'].insert(name, qobj)
            elif namespace in ('', 'global'):
                self._root.setContextProperty(name, qobj)
            else:
                # print(namespace, name, ':pv')
                if namespace not in self._namespaces:
                    self._namespaces[namespace] = Namespace()
                    self._root.setContextProperty(
                        namespace, self._namespaces[namespace]
                    )
                self._namespaces[namespace].insert(name, qobj)
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
            # if verbose:
            #     print(
            #         ':rp',
            #         '[dim]registered variant to qml:[/] [cyan]{}[/]'
            #         .format(
            #             name if namespace == '' else
            #             f'py.{name}' if namespace == 'global' else
            #             f'py.{namespace}.{name}'
            #         )
            #     )
        
        # elif issubclass(qobj, QObject):
        #     name = name or qobj.__name__
        #     qcls = qobj
            
        #     if namespace == '':
        #         raise Exception(
        #             'cannot register a class to anonymous namespace!'
        #         )
        #     elif namespace == 'global':
        #         raise Exception(
        #             'cannot register a class to global namespace!'
        #         )
        #     else:
        #         if QmlNamedElement:
        #             exec('QmlNamedElement(qname)(cls)', {
        #                 'QML_IMPORT_NAME'         : namespace,
        #                 'QML_IMPORT_MAJOR_VERSION': 1,
        #                 'QML_IMPORT_MINOR_VERSION': 0,
        #                 'QmlNamedElement'         : QmlNamedElement,
        #                 'qname'                   : name,
        #                 'cls'                     : qcls,
        #             })
        #         elif QmlElement:  # TODO: not tested
        #             qcls.__name__ = name
        #             exec('QmlElement(cls)', {
        #                 'QML_IMPORT_NAME'         : namespace,
        #                 'QML_IMPORT_MAJOR_VERSION': 1,
        #                 'QML_IMPORT_MINOR_VERSION': 0,
        #                 'QmlElement'              : QmlElement,
        #                 'cls'                     : qcls,
        #             })
        #         else:
        #             # noinspection PyTypeChecker
        #             qmlRegisterType(qcls, namespace, 1, 0, name)
        #     # if verbose:
        #     #     print(
        #     #         ':rp',
        #     #         'registered pytype class to qml: [cyan]{} > {}[/]'
        #     #         .format(namespace, name)
        #     #     )
        else:
            raise Exception()
        
        self.__hidden_ref[id(qobj)] = qobj
    
    def freeze(self) -> None:
        # self.__root.setContextProperty('py', self._namespaces['py'])
        pass
    
    def release(self) -> None:
        for v in tuple(self._namespaces.values()): del v  # noqa
        self._namespaces.clear()
        self._namespaces['py'] = Namespace()
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
