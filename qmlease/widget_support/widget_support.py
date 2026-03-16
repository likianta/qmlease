import typing as t
from uuid import uuid1

from lk_utils import dedent
from qtpy.QtGui import QFont
from qtpy.QtGui import QFontMetrics

from .layout_engine import layout
from .._env import IS_WINDOWS
from ..qtcore import QObject
from ..qtcore import bind_signal
from ..qtcore import Slot
from ..style import pyenum
from ..style import pystyle


class WidgetSupport(QObject):
    _font_metrics: QFontMetrics
    
    def __init__(self) -> None:
        super().__init__()
        font = QFont()
        font.setPixelSize(12)
        if IS_WINDOWS:
            font.setFamily('Microsoft YaHei UI')
        self._font_metrics = QFontMetrics(font)
    
    @Slot(object)
    def align_field_title_widths(self, column: QObject) -> None:
        field_items = []
        for item in column.children():
            if item.class_name == 'LKField2':
                field_items.append(item)
        longest_title_width = max(
            (self.estimate_line_width(x['title']) for x in field_items)
        )
        print(len(field_items), longest_title_width, ':v')
        for item in field_items:
            item['titleWidth'] = longest_title_width
    
    @Slot(object)
    def auto_size(self, item: QObject) -> None:
        layout.size_self(item)
        layout.align_children(item, item['alignment'])
    
    @Slot(str)
    @Slot(str, object)
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
    
    @Slot(str, result=dict)
    @Slot(dict, result=dict)
    def fill_sidebar_item(self, data: t.Union[str, dict]) -> dict:
        if isinstance(data, str):
            return {'text': data, 'icon': '', 'color': ''}
        else:
            # assert data['text']
            return {'text': '', 'icon': '', 'color': '', **data}
    
    @Slot(list, result=int)
    @Slot(list, int, result=int)
    def get_best_width(self, texts: t.Iterable[str], padding: int = 0) -> int:
        return max(map(self.estimate_line_width, texts)) + padding * 2
    
    @Slot(result=str)
    def generate_random_id(self) -> str:
        return uuid1().hex
    
    @Slot(object)
    def init_column(self, item: QObject) -> None:
        layout.size_self(item)
        assert item['alignment'] in (
            'left', 'right', 'hcenter', 'hfill'
        ), item['alignment']
        if item['alignment'] != 'left':
            layout.align_children(item, item['alignment'])
        if item['autoSize']:
            layout.size_children(item, 'vertical')
    
    @Slot(object)
    def init_ghost_border(self, item: QObject) -> None:
        assert len(item.children()) == 2
        child = item.children()[1]
        
        x = item['padding']
        if isinstance(x, int):
            paddings = (x,) * 4
        elif len(x) == 2:
            paddings = (x[0], x[1], x[0], x[1])
        else:
            paddings = tuple(x)
        print(x, paddings, ':v')
        
        layout.js_engine.wrapSize2(
            item.qobj,
            child.qobj,
            paddings[1] + paddings[3],  # hside
            paddings[0] + paddings[2],  # vside
        )
        
        if paddings[0]:
            child['y'] = paddings[0]
        if paddings[3]:
            child['x'] = paddings[3]
    
    @Slot(object)
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
    
    @Slot(object)
    def init_row(self, item: QObject) -> None:
        layout.size_self(item)
        assert item['alignment'] in (
            'top', 'bottom', 'vcenter', 'vfill'
        ), item['alignment']
        if item['alignment'] != 'top':
            layout.align_children(item, item['alignment'])
        if item['autoSize']:
            layout.size_children(item, 'horizontal')
    
    @Slot(object)
    @Slot(object, str)
    def inspect_size(self, item: QObject, remark: str = '') -> None:
        print(dedent(
            '''
            inspect {}:
                size: {} x {}
                implicit size: {} x {}
                children rect size: {} x {}
            '''.format(
                '{} ({})'.format(remark, item.class_name) if remark else
                item.class_name,
                *map(int, (
                    item['width'], item['height'],
                    item['implicitWidth'], item['implicitHeight'],
                    item['childrenRect'].width(), item['childrenRect'].height(),
                ))
            ), 4, False
        ))
    
    @Slot(object)
    def resize_row(self, item: QObject) -> None:
        layout.size_children(item, 'horizontal')


widget_support = WidgetSupport()
