# 几种 QML 动态执行函数方案的比较

<a id="20221210025247"></a>

关联: 

- `qmlease/qmlside/js_evaluator.py`
- `qmlease/qmlside/js_evaluator.qml`
- `qmlease/qmlside/qlogger.py`

## 方案 1: 使用 `QJSEngine.evaluate`

代码:

```python
from textwrap import dedent
from textwrap import indent

from qtpy.QtCore import QObject
from qtpy.QtQml import QJSEngine
...

class JsEvaluator(QObject):
    """
    https://doc.qt.io/qtforpython-5/PySide2/QtQml/QJSEngine.html
    """

    def __init__(self):
        super().__init__()
        self.engine = QJSEngine()
        self.engine.installExtensions(QJSEngine.AllExtensions)
    
    def eval_js(self, code: str, kwargs: dict = None) -> Any:
        last_frame = currentframe().f_back
        last_file = last_frame.f_code.co_filename
        last_line = last_frame.f_lineno
        
        if not kwargs:
            result = self.engine.evaluate(code, last_file, last_line)
        else:
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
    ...
```

优点:

1. `console.log` 打印的是 `<last_file>:<last_line>`, 方便调试.
2. 整个逻辑是清晰易懂的.

存在的问题:

1. `Qt.binding` 无效.
2. 写法有些繁琐.

## 方案 2: 通过 `QQmlComponent` 创建一个 `QQuickItem` 对象

代码:

```python
from qtpy.QtCore import QObject
from qtpy.QtQml import QQmlComponent
...

class JsEvaluator(QObject):
    
    def __init__(self):
        super().__init__()
        self._comp = None
        self.__qobj = None

    @property
    def _qobj(self) -> QObject:
        if self.__qobj is None:
            from ..application import app
            self._comp = QQmlComponent(app.engine, xpath('js_evaluator.qml'))
            self.__qobj = self.comp.create()
        return self.__qobj

    _param_placeholder = compile(r'\$\w+')

    def eval_js(self, code: str, kwargs: dict = None) -> Any:
        if not kwargs:
            return self._qobj.evaluate(code, ())
    
        formal_args = {k: f'args[{i}]' for i, k in enumerate(kwargs.keys())}
        actual_args = tuple(kwargs.values())
        code = self._param_placeholder.sub(
            lambda m: formal_args[m.group()[1:]], code
        )
        return self._qobj.evaluate(code, actual_args)
```

QML 代码:

```qml
// js_evaluator.qml
import QtQml

QtObject {
    function evaluate(code, args) {
        return eval(code)
    }
}
```

优点:

1. 可以使用 `Qt.binding`.

缺点:

1. `console.log` 打印的是 `<eval code>:1`, 不方便调试.

## 方案 3: 通过某种方法, 修改 `eval` 的上下文中的 `console` 对象

代码:

先看 qml 的代码:

```qml
// js_evaluator.qml
import QtQml

QtObject {
    function evaluate(code, args, console) {
        //                        ~~~~~~~ 注意这里
        return eval(code)
    }
    // 以及下面新增的函数
    function createCustomLogger(real_file) {
        const _console = console
        return {'log': (...args) => _console.log(real_file, ...args)}
    }
}
```

python 代码: 和方案 2 类似, 部分修改点用波浪线标出:

```python
from qtpy.QtCore import QObject
from qtpy.QtQml import QQmlComponent
...

class JsEvaluator(QObject):
    
    def __init__(self):
        super().__init__()
        self._comp = None
        self.__qobj = None
    
    @property
    def _qobj(self) -> QObject:
        if self.__qobj is None:
            from ..application import app
            self._comp = QQmlComponent(app.engine, xpath('js_evaluator.qml'))
            self.__qobj = self.comp.create()
        return self.__qobj
    
    _param_placeholder = compile(r'\$\w+')
    
    def eval_js(self, code: str, kwargs: dict = None) -> Any:
        last_frame = currentframe().f_back
        last_file = last_frame.f_code.co_filename
        last_line = last_frame.f_lineno
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        logger = self._qobj.createCustomLogger(last_file)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        if not kwargs:
            return self._qobj.evaluate(code, (), logger)
            #                                    ~~~~~~
        
        formal_args = {k: f'args[{i}]' for i, k in enumerate(kwargs.keys())}
        actual_args = tuple(kwargs.values())
        code = self._param_placeholder.sub(
            lambda m: formal_args[m.group()[1:]], code
        )
        return self._qobj.evaluate(code, actual_args, logger)
        #                                             ~~~~~~
```

优点:

1. `console.log` 打印指向真实的调用者.
2. 可以使用 `Qt.binding`.

缺点:

1. 当报错发生时, `console.log` 仍显示 `<eval code>:1`.
2. 参数来回转换, 造成了性能损失.
2. 代码繁琐.

---

## 最终选择

最终, 我们选择了方案 3, 并在它基础上做了一些扩展和优化. 具体请查看文首的 [关联代码](#20221210025247).
