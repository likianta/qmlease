from __future__ import annotations

from inspect import currentframe
from re import compile
from textwrap import dedent
from textwrap import indent
from typing import Any

from lk_utils import xpath
from qtpy.QtCore import QObject
from qtpy.QtQml import QJSEngine
from qtpy.QtQml import QQmlComponent

from .console import qml_console
from ..application import app
from ..qtcore.qobject import QObjectBaseWrapper


# noinspection PyUnresolvedReferences
class JsEvaluator(QObject):
    """
    - https://doc.qt.io/qtforpython-5/PySide2/QtQml/QJSEngine.html
    - docs/qml-eval-proposals.zh.md
    """
    _comp: QQmlComponent
    
    def __init__(self):
        super().__init__()  # type: ignore
        self.__qobj = None
    
    @property
    def engine(self) -> QJSEngine:
        return app.engine
    
    # noinspection PyArgumentList
    @property
    def _qobj(self) -> QObject:
        if self.__qobj is None:
            self._comp = QQmlComponent(app.engine, xpath('js_evaluator.qml'))
            self.__qobj = self._comp.create()
        return self.__qobj
    
    _param_placeholder = compile(r'\$\w+')
    
    def eval_js(self, code: str, kwargs: dict = None) -> Any:
        if 'console' in code:
            last_frame = currentframe().f_back
            last_file = last_frame.f_code.co_filename
            last_line = last_frame.f_lineno
            
            logger = self._qobj.createCustomLogger(
                '[file_id:{}]'.format(
                    qml_console.generate_file_id(last_file, last_line)
                )
            )
        else:
            logger = self._qobj.useDefaultLogger()
        
        if not kwargs:
            return self._qobj.evaluate(code, (), logger)
        
        formal_args = {k: f'args[{i}]' for i, k in enumerate(kwargs.keys())}
        actual_args = tuple(kwargs.values())
        code = self._param_placeholder.sub(
            lambda m: formal_args[m.group()[1:]], code
        )
        return self._qobj.evaluate(code, actual_args, logger)
    
    def eval_js_2(self, code: str, kwargs: dict = None) -> Any:
        last_frame = currentframe().f_back
        last_file = last_frame.f_code.co_filename
        last_line = last_frame.f_lineno
        
        if not kwargs:
            result = self.engine.evaluate(code, last_file, last_line)
        else:
            code = self._param_placeholder.sub(
                lambda m: m.group()[1:], code
            )
            func = self.engine.evaluate(dedent('''
                (({parameters}) => {{
                    {code}
                }})
            ''').strip().format(
                parameters=', '.join(kwargs.keys()),
                code=indent(dedent(code), '    '),
            ), last_file, last_line - 1)
            
            args = []
            for v in kwargs.values():
                if isinstance(v, QObjectBaseWrapper):
                    args.append(self.engine.newQObject(v.qobj))
                elif isinstance(v, QObject):
                    args.append(self.engine.newQObject(v))
                else:
                    args.append(v)
            result = func.call(args)  # noqa
        
        if result.isError():
            raise RuntimeError(result.toString())
        return result.toVariant()
    
    def eval_js_3(self, code: str, kwargs: dict = None) -> Any:
        last_frame = currentframe().f_back
        last_file = last_frame.f_code.co_filename
        last_line = last_frame.f_lineno
        
        code = self._param_placeholder.sub(
            lambda m: m.group()[1:], code
        )
        
        if not kwargs:
            result = self.engine.evaluate(code, last_file, last_line)
            if result.isError():
                raise RuntimeError(result.toString())
            return result.toVariant()
        else:
            code = dedent('''
                (({parameters}) => {{
                    {code}
                }})(...args)
            ''').strip().format(
                parameters=', '.join(kwargs.keys()),
                code=indent(dedent(code), '    '),
            )
            # print(':lv', code, kwargs)
            
            actual_args = [
                self.engine.newQObject(v.qobj) if isinstance(
                    v, QObjectBaseWrapper)
                else self.engine.newQObject(v) if isinstance(v, QObject)
                else v for v in kwargs.values()
            ]
            
            get_console = self.engine.evaluate(dedent('''
                () => {
                    const _log = console.log
                    return {'log': (...args) => _log(
                        '[file_id:$file_id]', ...args
                    )}
                }
            ''').strip().replace(
                '$file_id', qml_console.generate_file_id(last_file, last_line)
            ))
            console = get_console.call()
            
            return self._qobj.evaluate(code, actual_args, console)


js_eval = JsEvaluator()
eval_js = js_eval.eval_js_3
