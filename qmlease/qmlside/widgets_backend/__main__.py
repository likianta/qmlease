import typing as t
from functools import partial

from qtpy.QtCore import QRectF
from qtpy.QtGui import QFont
from qtpy.QtGui import QFontMetrics

from ..layout_helper import pylayout
from ..._env import IS_WINDOWS
from ...qtcore import QObject
from ...qtcore import bind_prop
from ...qtcore import bind_signal
from ...qtcore import slot
from ...style import pyenum
from ...style import pystyle


class WidgetBackend(QObject):
    _font_metrics: QFontMetrics
    
    def __init__(self) -> None:
        super().__init__()
        font = QFont()
        font.setPixelSize(12)
        if IS_WINDOWS:
            font.setFamily('Microsoft YaHei UI')
        self._font_metrics = QFontMetrics(font)
        
    def estimate_line_width(self, text: str, item_ref: QObject = None) -> int:
        if text == '':
            return 0
        if '\n' in text:
            text = max(text.splitlines(), key=len)
        
        if item_ref is None:
            metrics = self._font_metrics
        else:
            metrics = QFontMetrics(item_ref.property('font'))
        return int(metrics.horizontalAdvance(text) * 1.2)
    
    @slot(list, result=int)
    @slot(list, int, result=int)
    def get_best_width(self, texts: t.Iterable[str], padding: int = 0) -> int:
        return max(map(self.estimate_line_width, texts)) + padding * 2
    
    @slot(object)
    def init_radio_group(self, item: QObject) -> None:
        if item['horizontal']:
            if item['width'] == pyenum.AUTO:
                self._set_size_wrapped(item, 'width')
            if item['height'] == pyenum.AUTO:
                item['height'] = pystyle.size['item_height']
        else:
            if item['width'] == pyenum.AUTO:
                
                def wrap_model_width() -> None:
                    item['width'] = self.get_best_width(
                        (item['title'], *item['model']), item['spacing']
                    )
                    print(':v', 'finalize radio group width', item['width'])
                
                if item['model']:
                    wrap_model_width()
                else:
                    item.modelChanged.connect(wrap_model_width)
            
            if item['height'] == pystyle.AUTO:
                self._set_size_wrapped(item, 'height')
        
        @bind_signal(item.horizontalChanged)
        def _no_more_changed() -> None:
            print('LKRadioControl.horizontal should not be changed after its '
                  'instantiation!', ':v6')
    
    @slot(object)
    @slot(object, str)
    def size_children(
        self,
        item: QObject,
        strategy: t.Literal['default', 'row', 'column'] = 'default'
    ) -> None:
        _parent, _children = item, item.children()
        
        def size_children_widths() -> None:
            for child in _children:
                if child.property('width') == pyenum.STRETCH:
                    _bind_prop(_parent, child, 'width')
                    
        def size_children_heights() -> None:
            for child in _children:
                if child.property('height') == pyenum.STRETCH:
                    _bind_prop(_parent, child, 'height')
        
        def _bind_prop(src, dst, prop, effect_now: bool = True) -> None:
            getattr(dst, f'{prop}Changed').connect(
                partial(_set_prop, src, dst, prop)
            )
            if effect_now:
                dst[prop] = src[prop]
        
        def _set_prop(src, dst, prop) -> None:
            dst[prop] = src[prop]
        
        if strategy == 'default':
            size_children_widths()
            size_children_heights()
        elif strategy == 'row':
            pylayout.auto_size_children(item, 'h')
            size_children_heights()
        elif strategy == 'column':
            pylayout.auto_size_children(item, 'v')
            size_children_widths()
        
        # # noinspection PyUnresolvedReferences
        # cls_name = item.qobj.metaObject().className().split('_QMLTYPE_')[0]
        # #   e.g. 'LKRow_QMLTYPE_0' -> 'LKRow'
        #
        # if cls_name == 'LKRow':
        #     pylayout.auto_size_children(item, 'h')
        #     size_children_heights()
        # elif cls_name == 'LKColumn':
        #     pylayout.auto_size_children(item, 'v')
        #     size_children_widths()
        # else:
        #     size_children_widths()
        #     size_children_heights()
        
    @staticmethod
    def _set_size_wrapped(
        item: QObject, prop: t.Optional[t.Literal['width', 'height']] = None
    ) -> None:
        
        def sync_size(
            item: QObject,
            rect: QRectF,
            prop: t.Optional[t.Literal['width', 'height']]
        ) -> None:
            if prop == 'width':
                item['width'] = rect.width()
            elif prop == 'height':
                item['height'] = rect.height()
            else:
                item['width'] = rect.width()
                item['height'] = rect.height()
        
        bind_prop(
            item, 'childrenRect', item,
            custom_handler=partial(sync_size, item, prop=prop)
        )
        sync_size(item, item['childrenRect'], prop)
