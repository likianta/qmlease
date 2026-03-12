from ._imp import QObject
from ._imp import Slot


class Slider(QObject):
    
    @Slot(float, result=str)
    @Slot(float, int, result=str)
    def show_value(self, value: float, precison: int = 0) -> str:
        return f'{value * 100:.{precison}f}%'
