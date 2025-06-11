import typing as t
from functools import partial

from lk_utils import bind_with
from qtpy.QtGui import QFont
from qtpy.QtGui import QFontMetrics

from ..enum import pyenum
from ..qml_eval import qml_eval
from ..._env import IS_WINDOWS
from ...qtcore import QObject
from ...qtcore import bind_func  # noqa
from ...qtcore import slot


class T:
    # Orientation = t.Literal['h', 'horizontal', 'v', 'vertical']
    Orientation = t.Literal['h', 'v']


class LayoutHelper(QObject):
    
    def __init__(self) -> None:
        super().__init__()
        # see also `../../style/font.py`.
        font = QFont()
        font.setPixelSize(12)
        if IS_WINDOWS:
            font.setFamily('Microsoft YaHei UI')
        self._font_metrics = QFontMetrics(font)
    
    @slot(object, str)
    def init_view(
        self,
        container: QObject,
        type_: t.Literal['row', 'column']
    ) -> None:
        if type_ == 'row':
            orientation = 'h'
            size_prop = 'width'  # noqa
            another_size_prop = 'height'
            size_changed = 'width_changed'
        else:
            orientation = 'v'
            size_prop = 'height'  # noqa
            another_size_prop = 'width'
            size_changed = 'height_changed'
        
        if x := container['alignment']:
            self.auto_align(container, x)
            
            @bind_with(container[another_size_prop + '_changed'].connect)
            def _():
                self.auto_align(container, x)
        
        if container['autoSize']:
            self.auto_size_children(container, orientation)  # noqa
            
            # TODO: when children count changed, auto size again.
            @bind_with(container[size_changed].connect)
            def _():
                self.auto_size_children(container, orientation)  # noqa
    
    # -------------------------------------------------------------------------
    # new generation of auto alignment.
    
    # for LKHBox.qml
    @slot(object)
    def halign_children(self, hbox: QObject) -> None:
        self._resize_children(hbox, 'h')
        self._align_children(hbox, 'h')
    
    # for LKVBox.qml
    @slot(object)
    def valign_children(self, vbox: QObject) -> None:
        self._resize_children(vbox, 'v')
        self._align_children(vbox, 'v')
    
    @staticmethod
    def _align_children(box: QObject, orientation: T.Orientation) -> None:
        children = box.children()
        last = None
        
        if orientation == 'h':
            center = 'verticalCenter'
            side_0 = 'left'
            side_1 = 'right'
            padding_0 = (0, 0, 0, box['padding'])
            padding_1 = (0, box['padding'], 0, 0)
        else:
            center = 'horizontalCenter'
            side_0 = 'top'
            side_1 = 'bottom'
            padding_0 = (box['padding'], 0, 0, 0)
            padding_1 = (0, 0, box['padding'], 0)
        
        for i, child in enumerate(children):
            qml_eval.bind_anchors_to_parent(child, box, center)
            if i == 0:
                qml_eval.bind_anchors_to_parent(
                    child, box, side_0, padding_0
                )
            else:
                qml_eval.bind_anchors_to_sibling(
                    child, last, ((side_0, side_1),), box['spacing']
                )
                if i == len(children) - 1:
                    qml_eval.bind_anchors_to_parent(
                        child, box, side_1, padding_1
                    )
            last = child
    
    @staticmethod
    def _resize_children(box: QObject, orientation: T.Orientation) -> None:
        children = box.children()
        
        # stretch items in opposite direction
        def rstretch():
            prop_r = 'height' if orientation == 'h' else 'width'
            for child in children:
                if child.property(prop_r) == 0:
                    qml_eval.bind_prop(child, box, prop_r)
        
        if (
            (orientation == 'h' and box.property('vfill')) or
            (orientation == 'v' and box.property('hfill'))
        ):
            rstretch()
        
        # ---------------------------------------------------------------------
        # auto size children
        
        prop = 'width' if orientation == 'h' else 'height'
        # if container.property(prop_name) <= 0: return False
        
        elastic_items: dict[int, float] = {}  # dict[int index, float ratio]
        stretch_items: dict[int, int] = {}  # dict[int index, int _]
        #   note: stretch_items.values() are useless (they are all zeros). it -
        #   is made just for keeping the same form with elastic_items.
        
        claimed_size = 0
        for idx, item in enumerate(children):
            size = item.property(prop)
            if size >= 1:
                claimed_size += size
            elif 0 < size < 1:
                elastic_items[idx] = size
            elif size == 0 or size == -1:
                # FIXME: see reason in `self.auto_size_children : [code]
                #   size == -1`
                stretch_items[idx] = 0
            else:
                raise ValueError('cannot allocate negative size', idx, item)
        
        if not elastic_items and not stretch_items:
            return
        
        def get_total_available_size_for_children() -> int:
            return (
                box.property(prop) -
                box.property('padding') * 2 -
                box.property('spacing') * (len(children) - 1)
            )
        
        total_spare_size = get_total_available_size_for_children()
        unclaimed_size = total_spare_size - claimed_size
        
        if unclaimed_size <= 0:
            # fast finish leftovers
            for idx, item in enumerate(children):
                if idx in elastic_items:
                    item.setProperty(prop, 0)
                # note: no need to check if idx in stretch_items, because -
                # their size is already 0.
            return
        
        # allocate elastic items
        total_unclaimed_size = unclaimed_size
        for idx, ratio in elastic_items.items():
            child = children[idx]
            size = total_unclaimed_size * ratio
            child.setProperty(prop, size)
            unclaimed_size -= size
        
        if unclaimed_size <= 0:
            return
        if not stretch_items:
            return
        
        # allocate stretch items
        total_unclaimed_size = unclaimed_size
        stretch_items_count = len(stretch_items)
        stretch_item_size_aver = total_unclaimed_size / stretch_items_count
        for idx in stretch_items.keys():
            child = children[idx]
            child.setProperty(prop, stretch_item_size_aver)
    
    # -------------------------------------------------------------------------
    
    # DELETE
    # noinspection PyUnresolvedReferences
    @slot(object, str)
    def auto_align(self, container: QObject, alignment: str) -> None:
        """
        args:
            alignment: accept multiple options, separated by comma (no space
                between).
                for example: 'hcenter,stretch'
                options list:
                    hcenter: child.horizontalCenter = container.horizontalCenter
                    vcenter: child.verticalCenter = container.verticalCenter
                    hfill: child.with = container.width
                    vfill: child.height = container.height
                    stretch
        """
        children = container.children()
        
        for a in alignment.split(','):
            if a == 'hcenter':
                for child in children:
                    qml_eval.bind_anchors_to_parent(
                        child, container, 'horizontalCenter'
                    )
            
            elif a == 'vcenter':
                for child in children:
                    qml_eval.bind_anchors_to_parent(
                        child, container, 'verticalCenter'
                    )
            
            elif a == 'hfill' or a == 'vfill':
                def resize_children(orientation: str):
                    nonlocal container
                    prop = 'width' if orientation == 'h' else 'height'
                    for child in container.children():
                        child.setProperty(prop, container.property(prop))
                
                if a == 'hfill':
                    container.widthChanged.connect(
                        partial(resize_children, 'h')
                    )
                    container.widthChanged.emit()
                else:
                    container.heightChanged.connect(
                        partial(resize_children, 'v')
                    )
                    container.heightChanged.emit()
            
            elif a == 'stretch':
                container_type = self._detect_container_type(container)
                
                def stretch_children(orientation: str):
                    nonlocal container
                    prop = 'width' if orientation == 'h' else 'height'
                    children = container.children()
                    size_total = (container.property(prop)
                                  - container.property('spacing')
                                  * (len(children) - 1))
                    size_aver = size_total / len(children)
                    # print(':v', prop, size_total, size_aver)
                    for child in container.children():
                        child.setProperty(prop, size_aver)
                
                if container_type == 0:
                    container.widthChanged.connect(
                        partial(stretch_children, 'h')
                    )
                    container.widthChanged.emit()
                elif container_type == 1:
                    container.heightChanged.connect(
                        partial(stretch_children, 'v')
                    )
                    container.heightChanged.emit()
    
    @slot(object, str, result=bool)
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
        orientation: T.Orientation
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
    
    @slot('any', result=int)
    @slot('any', object, result=int)
    def calc_content_width(
        self,
        text: t.Union[str, t.List[str]],
        text_item: QObject = None,
    ) -> int:
        if text == '':
            return 0
        if isinstance(text, list):
            text = max(text, key=len)
        if '\n' in text:
            text = max(text.split('\n'), key=len)
        
        if text_item is None:
            fm = self._font_metrics
        else:
            fm = QFontMetrics(text_item.property('font'))
        return int(fm.horizontalAdvance(text) * 1.2)
    
    @slot(list, result=tuple)
    @slot(list, int, result=tuple)
    @slot(list, int, int, result=tuple)
    def calc_text_block_size(  # DELETE
        self,
        lines: t.List[str],
        char_width: int = 10,
        line_height: int = 20,
    ) -> t.Tuple[int, int]:
        lines = tuple(map(str, lines))
        # OPTM: use different char_width for non-ascii characters.
        width = max(map(len, lines)) * char_width
        height = (len(lines) + 1) * line_height
        return width, height
    
    @slot(object, str)
    def equal_size_children(self, container: QObject, orientation: str):
        # roughly equal size children
        children = container.children()
        if orientation in ('horizontal', 'h'):
            prop = 'width'
        else:
            prop = 'height'
        average_size = container.property(prop) / len(children)
        for item in children:
            item.setProperty(prop, average_size)
    
    @staticmethod
    def _detect_container_type(container: QObject) -> int:
        """
        return: 0 for row, 1 for column.
        help: if container is row, it has property 'effectiveLayoutDirection'
            (the value is Qt.LeftToRight(=0) or Qt.RightToLeft(=1)), while -
            column doesn't have this property(=None).
        """
        if container.property('effectiveLayoutDirection') is not None:
            return 0  # row
        else:
            return 1  # column


pylayout = LayoutHelper()
