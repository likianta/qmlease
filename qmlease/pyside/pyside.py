from __future__ import annotations

import typing as t

from .register import PyRegister
from ..qtcore import QObject
from ..qtcore import slot


class PySide(QObject, PyRegister):
    
    @slot(str, result=object)
    @slot(str, list, result=object)
    @slot(str, list, dict, result=object)
    def call(
            self,
            func_name: str,
            args: list = (),
            kwargs: dict = None
    ) -> t.Any:
        """ call python functions in qml side. """
        func, narg = self._pyfunc_holder[func_name]  # narg: 'number of args'
        if kwargs:
            return func(*args, **kwargs)
        elif narg == 0:
            return func()
        elif narg == -1:  # see `PyRegister._get_number_of_args.<return>`
            return func(*args)
        else:
            if isinstance(args, list) and narg > 1:
                return func(*args)
            else:  # experimental feature.
                return func(args)
    
    @slot(object, str, dict, result=object)
    def kwcall(self, qobj: QObject, method_name: str, kwargs: dict) -> t.Any:
        """
        usage:
            // qml side
            pyside.kwcall(lkutil, 'open_file_dialog', {'title': 'Open File'})
        """
        return getattr(qobj, method_name)(**kwargs)
    
    @slot(str, result=object)
    @slot(str, dict, result=object)
    def eval(self, code: str, kwargs: dict = None) -> t.Any:
        from textwrap import dedent, indent
        # print(':l', kwargs, '\n' in code)
        # print(code)
        
        if kwargs is None: kwargs = {}
        kwargs.update({'__file__': __file__})
        
        code_wrapper = dedent('''
            def __selfunc__():
                # the source code can use `__selfunc__` for recursive call.
                {source_code}
            __return_hook__ = __selfunc__()
        ''').format(source_code=indent(dedent(code), '    '))
        try:
            exec(code_wrapper, kwargs)
        except Exception as e:
            print(':lv4', code_wrapper, kwargs, e)
            raise e
        
        # if kwargs['__return_hook__'] is not None:
        #     print(kwargs['__return_hook__'])
        return kwargs['__return_hook__']
    
    @slot(str, name='def')
    def def_(self, code_block: str) -> None:
        import re
        from textwrap import dedent
        code_block = dedent(code_block)
        funcname = re.search(r'^def (\w+)', code_block).group(1)
        code_wrapper = dedent('''
            {source_code}
            __func_hook__ = {funcname}
        ''').format(source_code=code_block, funcname=funcname)
        exec(code_wrapper, hook := {})
        self.register(hook['__func_hook__'], name=funcname)


pyside = PySide()
register = pyside.register_via_decorator
