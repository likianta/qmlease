from __future__ import annotations

from collections import defaultdict
from functools import wraps
from inspect import signature


class T:
    from typing import Callable, Dict, Literal, Tuple
    
    PyFunction = Callable
    
    PyClassName = str
    PyMethName = str
    RegisteredName = str
    
    NArgs = int  # number of arguments
    Arg0 = Literal['', 'self', 'cls']
    
    PyClassHolder = Dict[
        PyClassName, Dict[
            PyMethName, Tuple[RegisteredName, NArgs]
        ]
    ]
    PyFuncHolder = Dict[RegisteredName, Tuple[PyFunction, NArgs]]


class PyRegister:
    strict_mode = True
    _pyclass_holder: T.PyClassHolder = defaultdict(lambda: defaultdict())
    _pyfunc_holder: T.PyFuncHolder = {}
    
    @staticmethod
    def _get_number_of_args(func: T.Callable, strip_self=False) -> T.NArgs:
        """
        References:
            https://stackoverflow.com/questions/3517892/python-list-function
                -argument-names
        
        Notes:
            1. Do not use `func.__code__.co_argcount|co_posonlyargcount
               |co_kwonlyargcount|co_nlocals`, none of them supports counting
               the fact number of `*args` or `**kwargs`.
            2. Here's an example shows how `inspect.signature` considers about
               parameter `self`:
                    >>> class AAA:
                    >>>     def mmm(self, x): pass
                    >>> from inspect import signature
                    >>> print(signature(AAA.mmm).parameters)
                    OrderedDict([('self', <Parameter 'self'),
                                 ('x', <Parameter 'x'>)])
                    >>> print(signature(AAA().mmm).parameters)
                    OrderedDict([('x', <Parameter "x">)])
        
        Returns:
            int[-1, >=0]
                -1: uncertain number of parameters, i.e. there exists `*args`
                    or `**kwargs`.
                >=0: ...
        """
        params = signature(func).parameters
        #   e.g. OrderedDict([
        #       ('x', <Parameter "x">),
        #       ('args', <Parameter "*args">),
        #       ('kwargs', <Parameter "**kwargs">)
        #   ])
        if any(str(v).startswith('*') for v in params.values()):
            return -1
        elif strip_self:
            return len(params) - 1
        else:
            return len(params)
    
    def _register(self, func, name: str, narg: int):
        if self.strict_mode and name in self._pyclass_holder:
            raise Exception('Function already registered', name)
        self._pyfunc_holder[name] = (func, narg)
    
    def _register_function(self, func, name, narg):
        self._register(name, func, narg)
    
    def _register_instance(self, instance):
        class_name = instance.__class__.__name__
        for method_name, (name, narg) in \
                self._pyclass_holder[class_name].items():
            #   the `name` equals to `method_name`, or an alias of `method_name`
            method = getattr(instance, method_name)
            self._register(method, name, narg)
    
    # exposed to external caller.
    register_instance = _register_instance
    
    def _register_method(self, method, name, narg):
        class_name = method.__qualname__.split('.')[-2]
        ''' Examples:
                class AAA:
                    def mmm(self):
                        pass
    
                    class BBB:
                        def nnn(self):
                            pass
    
                print(AAA.mmm.__qualname__)  # -> 'AAA.mmm'
                print(BBB.nnn.__qualname__)  # -> 'AAA.BBB.nnn'
            
            Notes:
                Do not use `class_name = method.__class__.__name__`, its value
                is always 'function'.
        '''
        method_name = method.__name__
        print(':v', class_name, method_name)
        if self.strict_mode and \
                method_name in self._pyclass_holder[class_name]:
            raise Exception('Method already registered', method_name)
        self._pyclass_holder[class_name][method_name] = (name, narg)
    
    def register(self, obj, name=''):
        """ Registering Python functions/methods to `.pyside.PySide.<namespace>`.
            Then it can be used in QML file via `PySide.call(<name>, <qml_args>)`.
        
        Args:
            obj: Union[Callable, object]
                Function, method or something callable. Or class instance.
                Use `type(obj).__name__` to see its value. If its value is one
                of the following:
                    'function'
                    'method'
                    'builtin_function_or_method'
                It means `obj` is callable; otherwise it is a class instance.
            name: A custom name for `obj`, if empty, use `obj.__name__` as
                default.
        
        References:
            https://medium.com/%40mgarod/dynamically-add-a-method-to-a-class-in
                -python-c49204b85bd6+&cd=3&hl=zh-CN&ct=clnk&gl=sg
            https://blog.csdn.net/Wu_Victor/article/details/84334814
        """
        name = name or obj.__name__
        if (t := type(obj).__name__) in ('function', 'method'):
            narg = self._get_number_of_args(obj)
            self._register(obj, name, narg)
        elif t == 'builtin_function_or_method':
            self._register(obj, name, -1)
        else:
            self._register_instance(obj)
        return name
    
    def register_via_decorator(self, name='', arg0: T.Arg0 = ''):
        """ A decorator for registering Python functions/methods to
            `.pyside.PySide.<namespace>`. Then it can be used in QML file via
            `PySide.call(<name>, <qml_args>)`.
                           |
        Args:              |
            name: Function name to be registered in `.pyside.PySide
                .<namespace>`, if empty, use the decorated function's
                `__name__` attribute.
            arg0: See `<current_docstring>.examples`.

        Examples:
            from declare_qml.pyside.register import PyRegister
            
            pyregister = PyRegister()
            reg = pyregister.register_via_decorator
            
            @reg()  # do not forget the brackets
            def aaa(): pass

            class XXX:
                @reg(arg0='self')
                def xxx(self): pass

                @reg(arg0='cls')
                @classmethod
                def yyy(cls): pass

                @reg()
                @staticmethod
                def zzz(): pass

        Notes:
            You cannot sign up class:
                @reg()  # wrong!
                class AAA: pass
        """
        
        def decorator(func):
            nonlocal name, arg0
            
            name = name or func.__name__
            narg = self._get_number_of_args(func, strip_self=bool(arg0))
            
            if arg0 == '':
                self._register(func, name, narg)
            elif arg0 == 'self':
                self._register_method(func, name, narg)
            elif arg0 == 'cls':
                # TODO: self._register_classmethod(func, name, narg)
                raise Exception('Registerinag classmethod is not supported yet')
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            return wrapper
        
        return decorator
