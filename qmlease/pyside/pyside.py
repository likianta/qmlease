import re
import typing as t

from lk_utils import textwrap as tw

from .register import PyRegister
from ..qtcore import Slot
from ..qtcore.qobject import QObject
from ..qtcore.qobject import QObjectDelegate
from ..qtcore.qobject import QtObject


class PySide(QObject, PyRegister):
    
    @Slot(str, result=object)
    @Slot(str, list, result=object)
    @Slot(str, list, dict, result=object)
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
    
    @Slot(object, str, dict, result=object)
    def kwcall(self, qobj: QObject, method_name: str, kwargs: dict) -> t.Any:
        """
        usage:
            // qml side
            pyside.kwcall(lkutil, 'open_file_dialog', {'title': 'Open File'})
        """
        return getattr(qobj, method_name)(**kwargs)
    
    @Slot(str, result=object)
    @Slot(str, dict, result=object)
    def eval(self, code: str, kwargs: dict = None) -> t.Any:
        def exec_code_object(code: str, context: dict) -> t.Any:
            for k, v in context.items():
                if isinstance(v, QtObject):
                    context[k] = QObjectDelegate(v)
            context['__file__'] = __file__
            context['__hook__'] = {'__result__': None}
            # assert "__hook__['__result__'] =" in code
            try:
                exec(code, context)
            except Exception as e:
                print(':v8', code)
                print(':v8l', {
                    k: v for k, v in context.items() if not k.startswith('__')
                })
                raise e
            return context['__hook__']['__result__']
        
        full_code = tw.wrap(
            '''
            def __selfunc__():
                # the source code can use `__selfunc__` for recursive call.
                {source_code}
            __hook__['__result__'] = __selfunc__()
            '''
        ).format(source_code=tw.wrap(code, 4))
        return exec_code_object(full_code, kwargs or {})
    
    @Slot(str, name='def')
    def def_(self, code_block: str) -> None:
        code_block = tw.wrap(code_block)
        funcname = re.search(r'^def (\w+)', code_block).group(1)
        code_wrapper = tw.wrap(
            '''
            {source_code}
            __func_hook__ = {funcname}
            '''
        ).format(source_code=code_block, funcname=funcname)
        exec(code_wrapper, hook := {})
        self.register(hook['__func_hook__'], name=funcname)


pyside = PySide()
register = pyside.register_via_decorator
