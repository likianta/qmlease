"""
TODO: this module is going to replace `../layout_helper/layout_helper.py`.
"""

import typing as t
from functools import partial

from lk_utils import xpath
from qtpy.QtCore import QRectF
from qtpy.QtQml import QJSEngine
from qtpy.QtQml import QQmlComponent
from qtpy.QtQml import QQmlEngine

from ..qtcore import QObject
from ..qtcore import bind_prop
from ..qtcore import bind_signal
from ..style import pyenum


class T:
    Alignment = t.Literal[
        'bottom', 'hcenter', 'hfill', 'left', 'right', 'top', 'vcenter', 'vfill'
    ]
    Orientation = t.Literal['horizontal', 'vertical']


class LayoutEngine:
    
    def __init__(self) -> None:
        self.engine = QQmlEngine()
        self.engine.installExtensions(QJSEngine.AllExtensions)  # noqa
        self._comp = None
        self.__qobj = None
    
    @property
    def js_engine(self) -> t.Any:
        return self._qobj
    
    @property
    def _qobj(self) -> t.Any:
        if self.__qobj is None:
            # laterly init when qml app is running.
            self._comp = QQmlComponent(
                self.engine, xpath('layout_supplement.qml')
            )
            if self._comp.isError():
                raise RuntimeError(self._comp.errorString())
            else:
                assert self._comp.isReady()
            self.__qobj = self._comp.create()
            assert self.__qobj
            # self._qobj.testHello()
        return self.__qobj
    
    def align_children(self, parent: QObject, alignment: T.Alignment) -> None:
        for child in parent.children():
            if alignment == 'hfill':
                bind_prop(child, 'width', parent, True)
            elif alignment == 'vfill':
                bind_prop(child, 'height', parent, True)
                self._qobj.alignChild(parent.qobj, child.qobj, 'vcenter')
            else:
                self._qobj.alignChild(parent.qobj, child.qobj, alignment)
    
    def size_children(
        self,
        item: QObject,
        dimension: t.Optional[T.Orientation] = None,
    ) -> None:
        if dimension is None:
            self.size_children(item, 'horizontal')
            self.size_children(item, 'vertical')
            return
        
        parent, children = item, item.children()
        # del item
        prop_name = 'width' if dimension == 'horizontal' else 'height'
        
        solid_items: t.Dict[int, int] = {}
        portioned_items: t.Dict[int, float] = {}  # dict[int index, float ratio]
        stretched_items: t.Dict[int, int] = {}  # dict[int index, int _]
        #   note: stretched_items.values() are useless (they are all zeros). -
        #   we use dict is just for keeping the same form with portioned_items.
        
        resize = partial(
            self._size_children,
            parent,
            dimension,
            solid_items,
            portioned_items,
            stretched_items,
        )
        
        def _solid_resize(idx, item, prop_name):
            solid_items[idx] = item[prop_name]
            resize()
        
        for idx, item in enumerate(children):
            size = item[prop_name]
            if size >= 1:
                solid_items[idx] = size
                getattr(item, f'{prop_name}Changed').connect(partial(
                    _solid_resize, idx, item, prop_name
                ))
            elif 0 < size < 1:
                portioned_items[idx] = size
            elif size == pyenum.STRETCH:
                stretched_items[idx] = size
            else:  # < 0
                raise Exception(idx, item, size)
        
        getattr(parent, f'{prop_name}Changed').connect(resize)
        resize()
    
    def size_self(self, item: QObject) -> None:
        for prop_name in ('width', 'height'):
            if item[prop_name] in (pyenum.AUTO, pyenum.WRAP):
                if item['implicit{}'.format(prop_name.capitalize())]:
                    self._qobj.inferSize(
                        item.qobj,
                        'horizontal' if prop_name == 'width' else 'vertical'
                    )
                else:
                    self._qobj.wrapSize(
                        item.qobj,
                        'horizontal' if prop_name == 'width' else 'vertical',
                        0
                    )
            # elif item[prop_name] == pyenum.STRETCH:
            #     bind_prop(item, prop_name, item.parent(), True)
            # elif 0 < item[prop_name] < 1:
            #     def _update(item, parent, prop, ratio):
            #         item[prop] = parent[prop] * ratio
            #
            #     bind_prop(
            #         item, prop_name, item.parent(), True,
            #         custom_handler=partial(
            #             _update, item, item.parent(), prop_name, item[prop_name]
            #         )
            #     )
    
    @staticmethod
    def size_wrapped(
        item: QObject,
        dimension: t.Optional[t.Literal['width', 'height']] = None
    ) -> None:
        @bind_signal(item.childrenRectChanged)
        def sync_size(rect: QRectF) -> None:
            # print(rect, ':v')
            if dimension == 'width':
                item['width'] = rect.width()
            elif dimension == 'height':
                item['height'] = rect.height()
            else:
                item['width'] = rect.width()
                item['height'] = rect.height()
        
        sync_size(item['childrenRect'])
        
    @staticmethod
    def _get_total_available_size_for_children(
        item: QObject,
        children_count: int,
        orientation: T.Orientation,
    ) -> int:
        # print(':lp', {p: item.property(p) for p in (
        #     'width', 'height', 'spacing', 'padding',
        #     'leftPadding', 'rightPadding', 'topPadding', 'bottomPadding'
        # )})
        if orientation == 'horizontal':
            return (
                item.property('width')
                - item.property('leftPadding')
                - item.property('rightPadding')
                - item.property('spacing') * (children_count - 1)
            )
        else:
            return (
                item.property('height')
                - item.property('topPadding')
                - item.property('bottomPadding')
                - item.property('spacing') * (children_count - 1)
            )
    
    def _size_children(
        self,
        container: QObject,
        orientation: T.Orientation,
        solid_items: t.Dict[int, int],
        portioned_items: t.Dict[int, float],
        stretched_items: t.Dict[int, int],
    ) -> None:
        if not portioned_items and not stretched_items:
            return
        
        prop_name = 'width' if orientation == 'horizontal' else 'height'
        
        children = container.children()
        total_spare_size = self._get_total_available_size_for_children(
            container, len(children), orientation
        )
        claimed_size = sum(solid_items.values())
        unclaimed_size = total_spare_size - claimed_size
        # print(
        #     container[prop_name], orientation, total_spare_size, claimed_size,
        #     unclaimed_size, len(children), portioned_items, stretched_items,
        #     ':vl'
        # )
        
        if unclaimed_size <= 0:
            # fast finish leftovers
            for idx in (*portioned_items.keys(), *stretched_items.keys()):
                children[idx][prop_name] = 0
            return
        
        # allocate elastic items
        total_unclaimed_size = unclaimed_size
        for idx, ratio in portioned_items.items():
            child = children[idx]
            size = total_unclaimed_size * ratio
            child[prop_name] = size
            unclaimed_size -= size
        
        if not stretched_items:
            return
        if unclaimed_size <= 0:
            for idx in stretched_items.keys():
                children[idx][prop_name] = 0
            return
        
        # allocate stretched items
        total_unclaimed_size = unclaimed_size
        items_count = len(stretched_items)
        item_size_aver = total_unclaimed_size / items_count
        for idx in stretched_items.keys():
            children[idx][prop_name] = item_size_aver


layout = LayoutEngine()
