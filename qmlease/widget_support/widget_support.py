import os
import typing as t
from uuid import uuid1
from collections import defaultdict

from lk_utils import dedent
from lk_utils import fs
from qtpy.QtGui import QFont
from qtpy.QtGui import QFontMetrics

from .layout_engine import layout
from .shadow_tree import ShadowTree
from .._env import IS_WINDOWS
from ..qmlside import ListModel
from ..qtcore import QObject
from ..qtcore import Slot
from ..qtcore import bind_signal
from ..style import pyenum
from ..style import pystyle

class Plugins:
    # FIXME (limitation): plugin's `__init__()` params must be empty
    factory: t.Dict[str, t.Type[QObject]] = {
        'shadow_tree': ShadowTree,
    }
    _instances: t.Dict[str, QObject]

    def __init__(self) -> None:
        self._instances = {}

    def __getitem__(self, key: str):
        if key not in self._instances:
            self._instances[key] = self.factory[key]()
        return self._instances[key]
    
    # def __getattr__(self, key: str):
    #     if key == 'factory':
    #         return super().__getattribute__(key)
    #     if not hasattr(self, key):
    #         if key in self.factory:
    #             setattr(self, key, self.factory[key]())
    #         else:
    #             raise AttributeError(
    #                 f'"{key}" is not registered in plugins factory'
    #             )
    #     return super().__getattribute__(key)


class WidgetSupport(QObject):
    plugins: Plugins
    _font_metrics: QFontMetrics
    
    def __init__(self) -> None:
        super().__init__()
        self.plugins = Plugins()
        # TODO: below may be moved to plugin part
        font = QFont()
        font.setPixelSize(12)
        if IS_WINDOWS:
            font.setFamily('Microsoft YaHei UI')
        self._font_metrics = QFontMetrics(font)
    
    # def __getattr__(self, name: str):
    #     if name.startswith('_'):
    #         return super().__getattr__(name)
    #     if name in ('plugins',):
    #         return super().__getattribute__(name)
    #     if name in self.plugins:
    #         if not hasattr(self, name):
    #             setattr(self, name, self.plugins[name]())
    #         return super().__getattribute__(name)
    #     return super().__getattr__(name)

    # def install_plugin(self, name, instance=None, force=False):
    #     if force or not hasattr(self, name):
    #         setattr(self, name, instance or self.plugins[name]())
    
    # --------------------------------------------------------------------------
    
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
    
    @Slot(object, object)
    def bind_shadow_tree_model(self, source_tree, target_tree):
        self.plugins['shadow_tree'].bind_model(source_tree, target_tree)

    @Slot(list, result=object)
    def convert_path_list_to_tree_model(self, paths: t.List[str]) -> ListModel:
        """
        note: the given `paths` are not sorted, and may contain duplicates.
        """
        print(sorted(paths)[:10], len(paths), ':vl')
        out = ListModel(('type', 'name', 'path', 'children'), auto_submit=False)
        root = fs.normpath(os.path.commonpath(paths))
        out.append({
            'type': 'folder',
            'name': fs.basename(root),
            'path': root,
            'children': ListModel(
                ('type', 'name', 'path', 'children'), auto_submit=False
            )
        })

        xdict = defaultdict(list)
        for p in sorted(frozenset(paths)):
            if p == root:
                continue
            a = p.removeprefix(root)
            b, c = a.rsplit('/', 1)
            # `b` could be '' or '/'-started string.
            xdict[b].append(c)

        def recurse(xlist, current_prefix):
            assert current_prefix in xdict, current_prefix
            for name in xdict[current_prefix]:
                path = root + current_prefix + '/' + name
                if fs.isdir(path):
                    xlist.append({
                        'type': 'folder',
                        'name': name,
                        'path': path,
                        'children': ListModel(
                            ('type', 'name', 'path', 'children'), 
                            auto_submit=False
                        )
                    })
                    recurse(xlist[-1]['children'], current_prefix + '/' + name)
                    xlist[-1]['children'].submit().always()
                else:
                    xlist.append({
                        'type': 'file',
                        'name': name,
                        'path': path,
                    })
        
        recurse(out[0]['children'], '')
        out[0]['children'].submit().always()
        out.submit().always()
        return out

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
    
    @Slot(list, result=int)
    def get_longest_text_width(self, texts: t.List[str]) -> int:
        return texts and max(map(self.estimate_line_width, texts)) or 0

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
