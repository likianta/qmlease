from typing import *

from qtpy.QtCore import QObject

from ..js_evaluator import eval_js
from ...qt_core import slot


class T:  # TypeHint
    
    class Anchors(TypedDict):
        reclines: Union[Tuple[int, int, int, int], str]
        #   examples:
        #       (1, 0, 1, 1): left(on), top(off), right(on), bottom(on).
        #       'ijkl': i=top, k=bottom, j=left, l=right.
        #   special values:
        #       (0, 0, 0, 0): center in parent.
        #       (1, 1, 1, 1): fill parent.
        #       'center': center in parent.
        #       'fill': fill parent.
        margins: Union[int, Tuple[int, int, int, int]]
    
    Reclines = Tuple[int, int, int, int]


class Anchors:
    
    @staticmethod
    def _normalize_reclines(reclines) -> T.Reclines:
        if isinstance(reclines, str):
            if reclines == 'center':
                return 0, 0, 0, 0
            elif reclines == 'fill':
                return 1, 1, 1, 1
            else:
                def _foo(letter) -> int:
                    if f'-{letter}' in reclines:
                        return -1
                    elif letter in reclines:
                        return 1
                    else:
                        return 0
                
                # noinspection PyTypeChecker
                return tuple(map(_foo, ('j', 'i', 'l', 'k')))
        else:
            return reclines
    
    @slot('qobject', 'qobject', 'any')
    def weak_anchors(self, this: QObject, that: QObject, anchors: T.Anchors):
        reclines = self._normalize_reclines(anchors['reclines'])
        is_center_mode = False
        
        x0 = this.property('x')
        y0 = this.property('y')
        w0 = eval_js('{}.childrenRect.width', this)
        h0 = eval_js('{}.childrenRect.height', this)
        x1 = that.property('x')
        y1 = that.property('y')
        w1 = eval_js('{}.childrenRect.width', that)
        h1 = eval_js('{}.childrenRect.height', that)
        
        if all(reclines):
            x0 = x1
            y0 = y1
            w0 = w1
            h0 = h1
        elif not any(reclines):
            is_center_mode = True
            x0 = w1 / 2 - w0 / 2
            y0 = h1 / 2 - h0 / 2
        else:
            if reclines[0]:
                if reclines[0] > 0:
                    x0 = x1
                else:
                    x0 = x1 + w1
            if reclines[1]:
                if reclines[1] > 0:
                    y0 = y1
                else:
                    y0 = y1 + h1
            if reclines[2]:
                if reclines[2] > 0:
                    w0 = w1
                else:
                    w0 = x1 + w1 - x0
            if reclines[3]:
                if reclines[3] > 0:
                    h0 = h1
                else:
                    y0 = y1 + h1 - y0
        
        if not is_center_mode:
            
            margins = anchors['margins']
            
            if isinstance(margins, int):
                x0 += margins
                y0 += margins
                w0 -= margins
                h0 -= margins
            else:
                x0 += margins[0]
                y0 += margins[1]
                w0 -= margins[2]
                h0 -= margins[3]
        
        this.setProperty('x', x0)
        this.setProperty('y', y0)
        this.setProperty('width', w0)
        this.setProperty('height', h0)
    
    @slot('qobject', 'qobject', 'any')
    def quick_anchors(self, this: QObject, that: QObject, anchors: T.Anchors):
        
        reclines = self._normalize_reclines(anchors['reclines'])
        
        if all(reclines):
            eval_js('{}.anchors.fill = {}', this, that)
        elif not any(reclines):
            eval_js('{}.anchors.centerIn = {}', this, that)
        else:
            if reclines[0]:
                if reclines[0] > 0:
                    eval_js(
                        '{}.anchors.left = Qt.binding(() => {}.left)',
                        this, that
                    )
                else:
                    eval_js(
                        '{}.anchors.left = Qt.binding(() => {}.right)',
                        this, that
                    )
            if reclines[1]:
                if reclines[1] > 0:
                    eval_js(
                        '{}.anchors.top = Qt.binding(() => {}.top)',
                        this, that
                    )
                else:
                    eval_js(
                        '{}.anchors.top = Qt.binding(() => {}.bottom)',
                        this, that
                    )
            if reclines[2]:
                if reclines[2] > 0:
                    eval_js(
                        '{}.anchors.right = Qt.binding(() => {}.right)',
                        this, that
                    )
                else:
                    eval_js(
                        '{}.anchors.right = Qt.binding(() => {}.left)',
                        this, that
                    )
            if reclines[3]:
                if reclines[3] > 0:
                    eval_js(
                        '{}.anchors.bottom = Qt.binding(() => {}.bottom)',
                        this, that
                    )
                else:
                    eval_js(
                        '{}.anchors.bottom = Qt.binding(() => {}.top)',
                        this, that
                    )
        
        margins = anchors['margins']
        
        if isinstance(margins, int):
            eval_js('{}.anchors.margins = {}', this, margins)
        else:
            eval_js('{}.anchors.leftMargin = {}', this, margins[0])
            eval_js('{}.anchors.topMargin = {}', this, margins[1])
            eval_js('{}.anchors.rightMargin = {}', this, margins[2])
            eval_js('{}.anchors.bottomMargin = {}', this, margins[3])
