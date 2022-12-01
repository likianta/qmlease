from __future__ import annotations

from typing import Any

from .__ext__ import QObject
from .__ext__ import slot


class Progress(QObject):
    
    @slot(float, dict, result=float)
    def get_nearest_progress(self, prog: float,
                             model: dict[float, Any]) -> float:
        # print(model, [type(k) for k in model], ':vl')
        return min(model.keys(), key=lambda x: abs(float(x) - prog))
    
    @slot(float, dict, result=str)
    def get_nearest_value(self, prog: float, model: dict[float, Any]) -> str:
        key = self.get_nearest_progress(prog, model)
        return str(model[key])
    
    @slot(float, result=str)
    @slot(float, int, result=str)
    def show_value(self, value: float, precison=0) -> str:
        return f'{value * 100:.{precison}f}%'
