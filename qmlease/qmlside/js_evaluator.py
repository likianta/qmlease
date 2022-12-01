from __future__ import annotations

from re import compile
from textwrap import dedent
from typing import Any

from qtpy.QtCore import QObject
from qtpy.QtQml import QQmlComponent


class T:
    class JsEvaluatorCore:
        # stub for `./js_evaluator_core.qml`
        
        @staticmethod
        def bind(t_obj: QObject, s_obj: QObject, expression: str): pass
        
        @staticmethod
        def connect_prop(*_, **__) -> Any: pass
        
        @staticmethod
        def create_component(_: str) -> QQmlComponent: pass
        
        @staticmethod
        def create_object(component: QQmlComponent,
                          container: QObject) -> QObject: pass
        
        @staticmethod
        def eval_js(code: str, args: list[QObject]): pass
        
        @staticmethod
        def test() -> str: pass


class JsEvaluator:
    core: T.JsEvaluatorCore
    
    def __init__(self):
        from lk_utils import xpath
        from ..application import app
        component = QQmlComponent(
            app.engine, xpath('js_evaluator_core.qml'),
            parent=app.root
        )
        qobject = component.create()
        self.core = qobject
        assert self.core
    
    _placeholder = compile(r'\$\w+')
    
    def eval_js(self, code: str, kwargs: dict = None):
        """
        usage:
            eval_js('''
                for (let i = 0; i < $total; i++) {
                    $num++
                    console.log($num)
                }
            ''', {'total': 10, 'num': 100})
        """
        if '\n' in code:
            code = dedent(code)
        
        args = list(kwargs.values())
        delegated_args = {
            k: f'args[{i}]'
            for i, k in enumerate((kwargs or {}).keys())
        }
        code = self._placeholder.sub(
            lambda m: delegated_args[m.group(0)[1:]], code
        )
        
        return self.core.eval_js(code, args)


js_eval = JsEvaluator()
eval_js = js_eval.eval_js
