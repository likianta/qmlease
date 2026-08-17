import typing as tp
from functools import partial

from lk_utils import tw
from lk_utils import fs
from qtpy.QtCore import QRectF
from qtpy.QtQml import QJSEngine
from qtpy.QtQml import QQmlComponent
from qtpy.QtQml import QQmlEngine

from ...qtcore import QObject
from ...qtcore import Signal
from ...qtcore import Slot
from ...qtcore import bind_prop
from ...style import pyenum


class LayoutEngine(QObject):
    def __init__(self) -> None:
        super().__init__()
        self._qml_engine = QQmlEngine()
        self.__helper = None  # defer initialization after application started

    @property
    def _helper(self) -> tp.Any:
        if self.__helper is None:
            comp = QQmlComponent(self._qml_engine, fs.here('layout_helper.qml'))
            if comp.isError():
                raise RuntimeError(comp.errorString())
            else:
                assert comp.isReady()
            self.__helper = comp.create()
            assert self.__helper
        return self.__helper

    @Slot(object, bool, result=bool)
    def compute_layout(self, parent: QObject, horizontal: bool) -> bool:
        if horizontal:
            main_dim = 'width'
            main_align = 'halign'
            cross_dim = 'height'
            cross_align = 'valign'
        else:
            main_dim = 'height'
            main_align = 'valign'
            cross_dim = 'width'
            cross_align = 'halign'

        if parent[main_align] == 'none' and parent[cross_align] == 'none':
            return False

        # children = parent.children()
        children = parent['data']
        print(children, ':nv')
        responsive = False

        match parent[main_align]:
            case 'none':
                pass
            case 'start':
                pass
            case 'stretch':
                total_spare_size = (
                    parent[main_dim]
                    - parent['leftPadding']
                    - parent['rightPadding']
                    - (
                        0
                        if len(children) <= 1
                        else parent['spacing'] * (len(children) - 1)
                    )
                )
                if total_spare_size > 0:
                    tobe_stretched_children = [
                        x
                        for x in children
                        if (
                            x[f'{main_dim}_backup']
                            if x.has_prop(f'{main_dim}_backup')
                            else x[main_dim]
                        )
                        == pyenum.STRETCH
                    ]
                    print(
                        len(children),
                        len(tobe_stretched_children),
                        total_spare_size,
                        # each_stretch_size,
                        ':ln',
                    )
                    if tobe_stretched_children:
                        each_stretch_size = total_spare_size / len(
                            tobe_stretched_children
                        )
                        if each_stretch_size >= 1:
                            for child in tobe_stretched_children:
                                if not child.has_prop(f'{main_dim}_backup'):
                                    child.set_prop(
                                        f'{main_dim}_backup', pyenum.STRETCH
                                    )
                                child[main_dim] = each_stretch_size
                            responsive = True
            case _:
                raise Exception('{}: {}'.format(main_align, parent[main_align]))

        match parent[cross_align]:
            case 'center':
                self._helper.alignChild(
                    parent.qobj,
                    child.qobj,
                    '{}center'.format('v' if horizontal else 'h'),
                )
            case 'none':
                pass
            case 'stretch':
                for child in children:
                    bind_prop(child, cross_dim, parent, True)
            case _:
                raise Exception(
                    '{}: {}'.format(cross_align, parent[cross_align])
                )

        return responsive

    @Slot(object)
    @Slot(object, str)
    @Slot(object, str, bool)
    def inspect_size(
        self,
        item: QObject,
        remark: str = '',
        include_children: bool = False,
        _level: int = 0,
    ) -> tp.Optional[str]:
        def try_to_get_children_rect_size(item):
            try:
                return '{} x {}'.format(
                    item['childrenRect'].width(),
                    item['childrenRect'].height(),
                )
            except AttributeError:
                return 'N/A'

        template = tw.dedent(
            """
            inspect {NAME}:
                size: {WIDTH} x {HEIGHT}
                implicit size: {IMPLICIT_WIDTH} x {IMPLICIT_HEIGHT}
                children rect size: {CHILDREN_RECT_SIZE}

                {CHILDREN_INSPECTION}
            """,
            indent=4,
            join_sep='\\',
            lstrip=False,
        )
        output = template.format(
            NAME='"{}" ({})'.format(remark, item.class_name)
            if remark
            else '`{}`'.format(item.class_name),
            WIDTH=item['width'],
            HEIGHT=item['height'],
            IMPLICIT_WIDTH=item['implicitWidth'],
            IMPLICIT_HEIGHT=item['implicitHeight'],
            CHILDREN_RECT_SIZE=try_to_get_children_rect_size(item),
            CHILDREN_INSPECTION=tw.join(
                self.inspect_size(
                    child,
                    include_children=True,
                    _level=_level + 1,
                )
                for child in item.children()
            ) if include_children else '',  # TODO
        ).rstrip()
        if _level == 0:
            print(output)
        else:
            return tw.indent(output, 4 * _level)


layout = LayoutEngine()
