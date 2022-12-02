from __future__ import annotations

import typing as t

from qtpy.QtCore import QObject as QObjectBase

from .signal_slot import slot


class QObject(QObjectBase):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def __getattr__(self, item):
        super().__getattribute__(item)
    
    @slot(name='__file__', result=str)
    def _self_path(self) -> str:
        return __file__
    
    def property(self, name: str) -> t.Any:
        return super().property(name)  # type: ignore
    
    def setProperty(self, name: str, value: t.Any) -> None:
        return super().setProperty(name, value)  # type: ignore


def get_children(self) -> list[QObjectBase]:
    """ a patch method for QObject.children().
    
    see only usage in [./signal_slot.py : def slot : def decorator : def
        func_wrapper].
    """
    out = []
    for i in QObjectBase.children(self):
        if i.property('enabled') is None:
            continue
        out.append(i)
    return out
