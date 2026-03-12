import typing as t

from ._imp import QObject
from ._imp import Slot


class Progress(QObject):
    
    @Slot(float, dict, result=float)
    def get_nearest_progress(
        self, prog: float, model: t.Dict[float, t.Any]
    ) -> float:
        # print(model, [type(k) for k in model], ':vl')
        return min(model.keys(), key=lambda x: abs(float(x) - prog))
    
    @Slot(float, dict, result=str)
    def get_nearest_value(
        self, prog: float, model: t.Dict[float, t.Any]
    ) -> str:
        key = self.get_nearest_progress(prog, model)
        return str(model[key])
    
    @Slot(float, result=str)
    @Slot(float, int, result=str)
    def show_value(self, value: float, precison: int = 0) -> str:
        return f'{value * 100:.{precison}f}%'
