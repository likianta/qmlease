import typing as t
import uuid

from qtpy.QtGui import QFont
from qtpy.QtGui import QFontMetrics

from .layout_engine import layout
from ..._env import IS_WINDOWS
from ...qtcore import QObject
from ...qtcore import bind_signal
from ...qtcore import slot
from ...style import pyenum
from ...style import pystyle


class WidgetSupport(QObject):
    _font_metrics: QFontMetrics
    
    def __init__(self) -> None:
        super().__init__()
        font = QFont()
        font.setPixelSize(12)
        if IS_WINDOWS:
            font.setFamily('Microsoft YaHei UI')
        self._font_metrics = QFontMetrics(font)
    
    # -------------------------------------------------------------------------
    
    @slot(object)
    def init_column(self, item: QObject) -> None:
        assert item['alignment'] in (
            'left', 'right', 'hcenter', 'hfill'
        ), item['alignment']
        layout.align_children(item, item['alignment'])
        if item['autoSize']:
            layout.size_children(item, 'column')
    
    @slot(object)
    def init_radio_group(self, item: QObject) -> None:
        if item['horizontal']:
            if item['width'] == pyenum.AUTO:
                layout.size_wrapped(item, 'width')
            if item['height'] == pyenum.AUTO:
                item['height'] = pystyle.size['item_height']
        else:
            if item['width'] == pyenum.AUTO:
                
                def wrap_model_width() -> None:
                    # print(
                    #     ':v',
                    #     item['title'],
                    #     item['model'],
                    #     item['width'],
                    #     self.get_best_width(
                    #         (item['title'], *item['model']), item['spacing']
                    #     )
                    # )
                    item['width'] = self.get_best_width(
                        (item['title'], *item['model']), item['spacing']
                    )
                    print(':v', 'finalize radio group width',
                          item['title'], item['width'])
                
                if item['model']:
                    wrap_model_width()
                else:
                    item.modelChanged.connect(wrap_model_width)
            
            if item['height'] == pyenum.AUTO:
                layout.size_wrapped(item, 'height')
        
        @bind_signal(item.horizontalChanged)
        def _no_more_changed() -> None:
            print('LKRadioControl.horizontal should not be changed after its '
                  'instantiation!', ':v6')
    
    @slot(object)
    def init_row(self, item: QObject) -> None:
        assert item['alignment'] in (
            'top', 'bottom', 'vcenter', 'vfill'
        ), item['alignment']
        layout.align_children(item, item['alignment'])
        if item['autoSize']:
            layout.size_children(item, 'row')
    
    @slot(object)
    @slot(object, str)
    def size_children(
        self,
        item: QObject,
        policy: t.Literal['default', 'row', 'column'] = 'default'
    ) -> None:
        layout.size_children(item, policy)
    
    # -------------------------------------------------------------------------
    # general
    
    @slot(str)
    @slot(str, object)
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
    
    @slot(result=str)
    def generate_random_id(self) -> str:
        return uuid.uuid1().hex


widget_support = WidgetSupport()
