import typing as t
from functools import partial

from .enum_ import pyenum
from ..qtcore import QObject
from ..qtcore import bind_func
from ..qtcore import slot


class T:
    # Orientation = t.Literal['h', 'horizontal', 'v', 'vertical']
    Orientation = t.Literal['h', 'v']


class LayoutEngine(QObject):
    
    @slot(object, str, result=bool)
    def auto_size_children(
            self,
            container: QObject,
            orientation: T.Orientation
    ) -> bool:
        """
        size policy:
            0: 0px as is.
            0 ~ 1: the ratio of spared space.
            1+: regular pixel point.
            pyenum.FILL: fill the rest space.

        workflow:
            1. get total space
            2. consume used space
            3. allocate unused space

        TODO: rename this method? (candidate names:)
            mobilize
            auto_pack

        return: is dynamical binding effective?
            True means whenever container's size changed, this method should be
            called again.
        """
        prop_name = 'width' if orientation in ('h', 'horizontal') else 'height'
        # if container.property(prop_name) <= 0: return False
        
        children = container.children()
        
        elastic_items = {}  # dict[int index, float ratio]
        stretch_items = {}  # dict[int index, int _]
        #   note: stretch_items.values() are useless (they are all zeros). it
        #   is made just for keeping the same type struct with elastic_items.
        
        claimed_size = 0
        for idx, item in enumerate(children):
            size = item.property(prop_name)
            if size >= 1:
                claimed_size += size
            elif 0 < size < 1:
                elastic_items[idx] = size
            elif size == pyenum.FILL:
                stretch_items[idx] = 0
            else:
                raise ValueError('unknown size policy', idx, item, size)
        
        if not elastic_items and not stretch_items:
            return False
        
        self._auto_size_children(
            container, orientation, claimed_size,
            elastic_items, stretch_items
        )
        
        # print(':l', 'overview container and children sizes:',
        #       (container.property('width'), container.property('height')),
        #       {(x.property('objectName') or 'child') + f'#{idx}': (
        #           x.property('width'), x.property('height')
        #       ) for idx, x in enumerate(children)})
        
        # TODO: if children count is changed, trigger this method again.
        bind_func(
            container, f'{prop_name}Changed',
            partial(
                self._auto_size_children,
                container=container,
                orientation=orientation,
                claimed_size=claimed_size,
                elastic_items=elastic_items,
                stretch_items=stretch_items,
            )
        )
        
        return True
    
    @slot(object, int, str)
    def auto_spacing(
            self,
            container: QObject,
            spacing_policy: int,
            orientation: T.Orientation,
    ):
        prop_name = 'width' if orientation in ('h', 'horizontal') else 'height'
        paddings = (
            ('leftPadding', 'rightPadding')
            if orientation in ('h', 'horizontal') else
            ('topPadding', 'bottomPadding')
        )
        children = container.children()
        
        if spacing_policy == pyenum.BETWEEN:
            claimed_size = sum(x.property(prop_name) for x in children)
            container.setProperty(prop_name, eval('{} - {} - {} - {}'.format(
                container.property(prop_name),
                container.property(paddings[0]),
                container.property(paddings[1]),
                claimed_size,
            )))


pylayout = LayoutEngine()
