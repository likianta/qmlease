from __future__ import annotations

from inspect import currentframe
from re import compile
from textwrap import dedent
from textwrap import indent
from typing import Any

from lk_utils import xpath
from qtpy.QtCore import QObject
from qtpy.QtQml import QJSEngine

from ..qtcore.qobject import QObjectBaseWrapper


class JsEvaluator(QObject):
    """
    https://doc.qt.io/qtforpython-5/PySide2/QtQml/QJSEngine.html
    """
    engine: QJSEngine
    
    def __init__(self):
        super().__init__()  # type: ignore
        self.engine = QJSEngine()
        # self.engine.installExtensions(QJSEngine.ConsoleExtension)
        self.engine.installExtensions(QJSEngine.AllExtensions)
        #   use `AllExtensions` to introduce `Qt` object, etc.
        self.module = self.engine.importModule(xpath('js_evaluator.mjs'))
        # self.module.property('test_echo').call(
        #     ['[qmlease]/qmlside/js_evaluator.py : hello world']
        # )
    
    # DELETE: patch for legacy code. remove this in future.
    _code_compat_patch = compile(r'\$\w+')
    
    def eval_js(self, code: str, kwargs: dict = None) -> Any:
        """
        usage:
            eval_js('''
                for (let i = 0; i < total; i++) {
                    num++
                    console.log(num)
                }
                return num
            ''', {'total': 10, 'num': 100})
        """
        last_frame = currentframe().f_back
        last_file = last_frame.f_code.co_filename
        last_line = last_frame.f_lineno
        
        if not kwargs:
            result = self.engine.evaluate(code, last_file, last_line)
        else:
            code = self._code_compat_patch.sub(lambda m: m.group()[1:], code)
            func = self.engine.evaluate(dedent('''
                (({parameters}) => {{
                    {code}
                }})
            ''').strip().format(
                parameters=', '.join(kwargs.keys()),
                code=indent(dedent(code), '    '),
            ), last_file, last_line - 1)
            
            #: A
            # result = func.call([
            #     self.engine.newQObject(x.qobj)
            #     if isinstance(x, QObjectBaseWrapper)
            #     else self.engine.newQObject(x) if isinstance(x, QObject)
            #     else x
            #     for x in kwargs.values()
            # ])
            
            #: B
            args = []
            for v in kwargs.values():
                if isinstance(v, QObjectBaseWrapper):
                    args.append(self.engine.newQObject(v.qobj))
                elif isinstance(v, QObject):
                    args.append(self.engine.newQObject(v))
                else:
                    args.append(v)
            result = func.call(args)
        
        if result.isError():
            raise RuntimeError(result.toString())
        return result.toVariant()


js_eval = JsEvaluator()
eval_js = js_eval.eval_js
