import re
import typing as t
from inspect import currentframe

from lk_utils import xpath
from lk_utils.textwrap import dedent
from lk_utils.textwrap import reindent
from qtpy.QtCore import QObject
from qtpy.QtQml import QJSEngine
from qtpy.QtQml import QQmlComponent
from qtpy.QtQml import QQmlEngine

from ..qtcore import bind_signal
from ..qtcore.qobject import QObjectBaseWrapper


class T:
    AnchorsA = t.Optional[t.Literal[
        'centerIn', 'fill',
        'top', 'right', 'bottom', 'left',
        'hcenter', 'vcenter',
    ]]
    
    AnchorsB0 = t.Literal[
        'top', 'right', 'bottom', 'left',
        'hcenter', 'vcenter',
    ]
    AnchorsB1 = t.Union[
        t.Iterable[
            t.Union[
                AnchorsB0,
                t.Tuple[AnchorsB0, AnchorsB0]
            ]
        ], str, None
    ]
    AnchorsB2 = t.List[
        t.Tuple[AnchorsB0, AnchorsB0]
    ]
    
    Margins = t.Union[
        int,
        t.Tuple[int, int],
        t.Tuple[int, int, int, int],
        None
    ]
    
    ParamSpec = t.ParamSpec('ParamSpec')  # TODO
    QObject = t.Union[QObject, QObjectBaseWrapper]


class QmlEval(QObject):
    engine: QQmlEngine
    _comp: t.Optional[QQmlComponent]
    _qobj: t.Optional[QObject]
    
    def __init__(self):
        super().__init__(None)
        # self.engine = app.engine
        self.engine = QQmlEngine()
        self.engine.installExtensions(QJSEngine.AllExtensions)
        self._comp = None
        self._qobj = None
    
    @property
    def qobj(self) -> QObject:
        if self._qobj is None:
            self._comp = QQmlComponent(self.engine, xpath('qml_eval.qml'))
            if self._comp.isError():
                raise RuntimeError(self._comp.errorString())
            else:
                assert self._comp.isReady()
            self._qobj = self._comp.create()  # noqa
            assert self._qobj
            # self._qobj.testHello()
        return self._qobj
    
    _param_placeholder = re.compile(r'\$\w+')
    
    def eval_js(self, code: str, kwargs: dict = None) -> t.Any:
        last_frame = currentframe().f_back
        last_file = last_frame.f_code.co_filename
        last_line = last_frame.f_lineno
        
        if not kwargs:
            result = self.engine.evaluate(code, last_file, last_line)
        else:
            code = self._param_placeholder.sub(
                lambda m: m.group()[1:], code
            )
            func = self.engine.evaluate(dedent(
                '''
                (({parameters}) => {{
                    {code}
                }})
                '''
            ).format(
                parameters=', '.join(kwargs.keys()),
                code=reindent(code, 4),
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
    
    # -------------------------------------------------------------------------
    
    @staticmethod
    def bind_prop(
        a: T.QObject,
        b: T.QObject,
        prop: str,
        func: t.Optional[t.Callable] = None,
    ) -> None:
        if isinstance(a, QObjectBaseWrapper):
            a = a.qobj
        if isinstance(b, QObjectBaseWrapper):
            b = b.qobj
        
        if func:
            eval(f'b.{prop}Changed', {'b': b}).connect(func)
        else:
            @bind_signal(eval(f'b.{prop}Changed', {'b': b}))
            def _() -> None:
                a.setProperty(prop, b.property(prop))
    
    # -------------------------------------------------------------------------
    
    def bind_anchors_to_parent(
        self,
        child: T.QObject,
        parent: T.QObject,
        anchors: T.AnchorsA,
        margins: T.Margins = None,
    ) -> None:
        if isinstance(child, QObjectBaseWrapper):
            child = child.qobj
        if isinstance(parent, QObjectBaseWrapper):
            parent = parent.qobj
        self.qobj.bindAnchorsToParent(child, parent, anchors, margins)
    
    bind_anchors = bind_anchors_to_parent
    
    _split_anchors = re.compile(r'[,; ]+')
    
    def bind_anchors_to_sibling(
        self,
        one: T.QObject,
        another: T.QObject,
        anchors: T.AnchorsB1,
        margins: T.Margins = None,
    ):
        if isinstance(one, QObjectBaseWrapper):
            one = one.qobj
        if isinstance(another, QObjectBaseWrapper):
            another = another.qobj
        
        norm_anchors: T.AnchorsB2 = []
        if anchors:
            if isinstance(anchors, str):
                for x in self._split_anchors.split(anchors):
                    if '-' in x:
                        a, b = x.split('-')
                    else:
                        a = b = x
                    norm_anchors.append((a, b))
            else:
                for a in anchors:
                    if isinstance(a, tuple):
                        norm_anchors.append(a)
                    else:
                        norm_anchors.append((a, a))
        if norm_anchors:
            norm_anchors = [
                'horizontalCenter' if x == 'hcenter'
                else 'verticalCenter' if x == 'vcenter'
                else x
                for x in norm_anchors
            ]
        self.qobj.bindAnchorsToSibling(one, another, norm_anchors, margins)


qml_eval = QmlEval()
eval_js = qml_eval.eval_js
