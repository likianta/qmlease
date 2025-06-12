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

from ...qtcore import QObject
from ...qtcore import bind_func
from ...qtcore import bind_prop
from ...qtcore import bind_signal
from ...style import pyenum


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
                bind_prop(parent, 'width', child)
            elif alignment == 'vfill':
                bind_prop(parent, 'height', child)
                self._qobj.centerChild(parent.qobj, child.qobj, 'vcenter')
            else:
                self._qobj.centerChild(parent.qobj, child.qobj, alignment)
    
    def auto_size_children(
        self,
        container: QObject,
        orientation: T.Orientation
    ) -> bool:
        """
        size policy:
            0: auto stretch to spared space.
            0 ~ 1: the ratio of spared space.
            1+: regular pixel point.

        workflow:
            1. get total space
            2. consume used space
            3. allocate unused space

        TODO: method rename (candidate names):
            mobilize
            auto_pack

        return: is dynamical binding effective?
            True means whenever container's size changed, this method should -
            be called again.
        """
        prop_name = 'width' if orientation in ('h', 'horizontal') else 'height'
        
        children = container.children()
        
        portioned_items: dict[int, float] = {}  # dict[int index, float ratio]
        stretched_items: dict[int, int] = {}  # dict[int index, int _]
        #   note: stretched_items.values() are useless (they are all zeros). it
        #   is made just for keeping the same form with portioned_items.
        
        claimed_size = 0
        for idx, item in enumerate(children):
            size = item.property(prop_name)
            if size >= 1:
                claimed_size += size
            elif 0 < size < 1:
                portioned_items[idx] = size
            elif size in (0, -1, pyenum.STRETCH, pyenum.FILL):
                #   FIXME: too many magic numbers, leave only `pyenum.STRETCH`.
                """
                why `size == -1`?
                    this is a workaround.
                    for some widgets, their size default is 0, and they will -
                    resize themselves to a proper width in their `onCompleted` -
                    stage (based on their final content length).
                    to avoid triggering their auto resize policy, we cannot -
                    give them zero at the start. so we have to seek a solution -
                    like this.
                    i'm diggering qml mechanism, maybe we can find a better -
                    solution in future.
                """
                stretched_items[idx] = 0
            else:
                raise ValueError('cannot allocate negative size', idx, item)
        
        if not portioned_items and not stretched_items:
            return False
        
        self._auto_size_children(
            container,
            orientation,
            claimed_size,
            portioned_items,
            stretched_items,
        )
        
        # TODO: if children count is changed, trigger this method again.
        bind_func(
            container, f'{prop_name}Changed',
            partial(
                self._auto_size_children,
                container,
                orientation,
                claimed_size,
                portioned_items,
                stretched_items,
            )
        )
        return True
    
    def size_children(
        self,
        item: QObject,
        policy: t.Literal['default', 'row', 'column'] = 'default'
    ) -> None:
        _parent, _children = item, item.children()
        
        def size_children_widths() -> None:
            for child in _children:
                if child.property('width') == pyenum.STRETCH:
                    bind_prop(_parent, 'width', child, effect_now=True)
        
        def size_children_heights() -> None:
            for child in _children:
                if child.property('height') == pyenum.STRETCH:
                    bind_prop(_parent, 'height', child, effect_now=True)
        
        if policy == 'default':
            size_children_widths()
            size_children_heights()
        elif policy == 'row':
            self.auto_size_children(item, 'horizontal')
            size_children_heights()
        elif policy == 'column':
            self.auto_size_children(item, 'vertical')
            size_children_widths()
    
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
        
    def _auto_size_children(
        self,
        container: QObject,
        orientation: T.Orientation,
        claimed_size: int,
        portioned_items: t.Dict[int, float],
        stretched_items: t.Dict[int, int],
    ) -> None:
        """
        note: `stretched_items.values()` are useless (they are all zeros), we -
        make stretched_items dict type just for harmonizing the form with -
        portioned_items.
        """
        prop_name = 'width' if orientation in ('h', 'horizontal') else 'height'
        
        children = container.children()
        total_spare_size = self._get_total_available_size_for_children(
            container, len(children), orientation)
        unclaimed_size = total_spare_size - claimed_size
        # print(container.property(prop_name), total_spare_size, claimed_size,
        #       unclaimed_size, orientation, len(children), ':l')
        
        if unclaimed_size <= 0:
            # fast finish leftovers
            for idx, item in enumerate(children):
                if idx in portioned_items:
                    item.setProperty(prop_name, 0)
                # note: no need to check if idx in stretch_items, because -
                # their size is already 0.
            return
        
        # allocate elastic items
        total_unclaimed_size = unclaimed_size
        for idx, ratio in portioned_items.items():
            child = children[idx]
            size = total_unclaimed_size * ratio
            child.setProperty(prop_name, size)
            unclaimed_size -= size
        
        if unclaimed_size <= 0:
            return
        if not stretched_items:
            return
        
        # allocate stretched items
        total_unclaimed_size = unclaimed_size
        items_count = len(stretched_items)
        item_size_aver = total_unclaimed_size / items_count
        for idx in stretched_items.keys():
            child = children[idx]
            child.setProperty(prop_name, item_size_aver)
    
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
        if orientation in ('h', 'horizontal'):
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


layout = LayoutEngine()
