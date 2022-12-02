from textwrap import dedent
from textwrap import indent

from qtpy.QtCore import QObject
from qtpy.QtQml import QQmlPropertyMap

from ..js_evaluator import eval_js
from ..js_evaluator import js_eval
from ...qtcore import slot


class T:
    from qtpy.QtCore import QObject


class Enum:
    HORIZONTAL = 0
    VERTICAL = 1
    STRETCH = -1
    SHRINK = -2


class ContainerAlignment(QQmlPropertyMap):
    
    def __init__(self):
        super().__init__()
        for k in dir(Enum):
            if k.isupper() and not k.startswith('_'):
                self.insert(k, getattr(Enum, k))
    
    @slot(object, int)
    def auto_layout(self, container: QObject, orientation: int):
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
        """
        prop_name = 'width' if orientation == Enum.HORIZONTAL else 'height'
        if not container.property(prop_name): return
        total_size = self._get_total_available_size_for_children(
            container, orientation)
        item_sizes = {}  # dict[int index, float size]
        
        unclaimed_size = total_size
        for idx, item in enumerate(container.children()):
            print(idx, item.property('objectName'))
            size = item.property(prop_name)
            if size < 0:
                raise ValueError('cannot allocate negative size', idx, item)
            if size >= 1:
                item_sizes[idx] = size
                unclaimed_size -= size
        
        def fast_finish_leftovers():
            for idx, item in enumerate(container.children()):
                if idx not in item_sizes:
                    item.setProperty(prop_name, 0)
        
        if unclaimed_size <= 0:
            fast_finish_leftovers()
            return
        
        total_unclaimed_size = unclaimed_size
        for idx, item in enumerate(container.children()):
            size = item.property(prop_name)
            if idx not in item_sizes:
                if 0 < size < 1:
                    ratio = size
                    item_sizes[idx] = size = total_unclaimed_size * ratio
                    unclaimed_size -= size
        
        if unclaimed_size <= 0:
            fast_finish_leftovers()
            return
        
        left_count = len(container.children()) - len(item_sizes)
        left_size_average = unclaimed_size / left_count
        for idx, item in enumerate(container.children()):
            if idx not in item_sizes:
                item.setProperty(prop_name, left_size_average)
    
    @staticmethod
    def _get_total_available_size_for_children(
            item: QObject, orientation: int) -> int:
        if orientation == Enum.HORIZONTAL:
            return (
                    item.property('width')
                    - item.property('leftPadding')
                    - item.property('rightPadding')
                    - item.property('spacing') * (len(item.children()) - 1)
            )
        else:
            return (
                    item.property('height')
                    - item.property('topPadding')
                    - item.property('bottomPadding')
                    - item.property('spacing') * (len(item.children()) - 1)
            )
    
    # --------------------------------------------------------------------------
    # TODO: need review and refactor below
    
    @slot('qobject')
    def halign_center(self, parent: T.QObject):
        """ Align children in a Enum.HORIZONTAL line. """
        for item in parent.get_children():
            eval_js('{}.anchors.Enum.VERTICALCenter '
                    '= Qt.binding(() => {}.Enum.VERTICALCenter)',
                    item, parent)
    
    @slot('qobject')
    def valign_center(self, parent: T.QObject):
        """ Align children in a Enum.VERTICAL line. """
        for item in parent.get_children():
            eval_js('{}.anchors.Enum.HORIZONTALCenter '
                    '= Qt.binding(() => {}.Enum.HORIZONTALCenter)',
                    item, parent)
    
    # --------------------------------------------------------------------------
    
    @slot('qobject', int, int)
    def halign_children(self, parent: T.QObject, padding: int, spacing: int):
        self._align_children(parent, padding, spacing, Enum.HORIZONTAL)
    
    @slot('qobject', int, int)
    def valign_children(self, parent: T.QObject, padding: int, spacing: int):
        self._align_children(parent, padding, spacing, Enum.VERTICAL)
    
    @staticmethod
    def _align_children(parent: T.QObject, padding: int, spacing: int,
                        orientation: int):
        children = list(parent.get_children())
        if len(children) == 0:
            return
        
        if orientation == Enum.HORIZONTAL:
            eval_js(
                '{{0}}.anchors.leftMargin = {}'.format(padding),
                children[0]
            )
            eval_js(
                '{{0}}.anchors.rightMargin = {}'.format(padding),
                children[-1]
            )
        else:
            eval_js(
                '{{0}}.anchors.topMargin = {}'.format(padding),
                children[0]
            )
            eval_js(
                '{{0}}.anchors.bottomMargin = {}'.format(padding),
                children[-1]
            )
        
        prop = 'width' if orientation == Enum.HORIZONTAL else 'height'
        size = (
                parent.property(prop)
                - padding * 2
                - spacing * (len(children) - 1)
        )
        
        for i in children:
            i.setProperty(prop, size)
        
        if len(children) > 1:
            for a, b in zip(children[:-1], children[1:]):
                js_eval.quick_bind(b, 'anchors.left', a, 'right')
                eval_js('{0}.anchors.leftMargin', spacing)
    
    # --------------------------------------------------------------------------
    
    @slot('qobject')
    @slot('qobject', bool)
    def hadjust_children_size(self, parent: T.QObject, constraint=True):
        self._auto_adjust_children_size(parent, Enum.HORIZONTAL, constraint)
    
    @slot('qobject')
    @slot('qobject', bool)
    def vadjust_children_size(self, parent: T.QObject, constraint=True):
        self._auto_adjust_children_size(parent, Enum.VERTICAL, constraint)
    
    def _auto_adjust_children_size(
            self, parent: T.QObject, orientation: int, constraint: bool
    ):
        def _adjust(prop_name, unallocated_space):
            dynamic_sized_items_a = []  # type: list[tuple[QObject, float]]
            dynamic_sized_items_b = []  # type: list[tuple[QObject, float]]
            
            for i, item in enumerate(children):
                size = item.property(prop_name)
                if 0 < size < 1:
                    dynamic_sized_items_a.append((item, size))
                elif size == 0:
                    dynamic_sized_items_b.append((item, size))
                else:
                    unallocated_space -= size
            
            # ------------------------------------------------------------------
            
            if not dynamic_sized_items_a + dynamic_sized_items_b:
                return
            if unallocated_space <= 0:
                raise Exception('No space for allocating left children')
            if (declared_ratio := sum(x[1] for x in dynamic_sized_items_a)) > 1:
                raise Exception('The total size of dynamic items exceed '
                                'available space', declared_ratio,
                                unallocated_space)
            if declared_ratio == 1 and dynamic_sized_items_b:
                raise Exception('Cannot make space for size-undeclared items')
            
            if dynamic_sized_items_b:
                default_size_for_undefined_items = (
                        (1 - declared_ratio) / len(dynamic_sized_items_b)
                )
                dynamic_sized_items_b = [
                    (item, default_size_for_undefined_items)
                    for item, _ in dynamic_sized_items_b
                ]
            
            for item, ratio in dynamic_sized_items_a + dynamic_sized_items_b:
                if not constraint:
                    item.setProperty(prop_name, unallocated_space * ratio)
                else:
                    eval_js(dedent('''
                        {{0}}.{prop_name} = Qt.binding(() => {{{{
                            {js_expression}
                        }}}})
                    ''').format(
                        prop_name=prop_name,
                        js_expression=indent(dedent('''
                            let unallocated_space =
                                {{1}}.{prop_name} - {fixed_used_size}
                            return unallocated_space * {ratio}
                        '''.format(
                            prop_name=prop_name,
                            fixed_used_size=(parent.property(prop_name)
                                             - unallocated_space),
                            ratio=ratio,
                        )), ' ' * 4).strip()
                    ), item, parent)
        
        paddings = self._get_paddings(parent)
        spacing = parent.property('spacing')
        
        children = parent.get_children()
        # lk.logp([x.property('objectName') for x in children])
        
        if orientation == Enum.HORIZONTAL:
            _adjust(
                prop_name='width',
                unallocated_space=(
                        parent.property('width')
                        - (paddings[0] + paddings[2])
                        - spacing * (len(children) - 1)
                )
            )
        
        elif orientation == Enum.VERTICAL:
            _adjust(
                prop_name='height',
                unallocated_space=(
                        parent.property('height')
                        - (paddings[1] + paddings[3])
                        - spacing * (len(children) - 1)
                )
            )
    
    @staticmethod
    def _get_paddings(qobj: T.QObject):
        # return: tuple[left, top, right, bottom]
        return (
            qobj.property('leftPadding'),
            qobj.property('topPadding'),
            qobj.property('rightPadding'),
            qobj.property('bottomPadding'),
        )
