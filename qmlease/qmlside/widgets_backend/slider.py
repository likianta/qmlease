from .__ext__ import QObject
from .__ext__ import slot


class Slider(QObject):
    
    @slot(float, result=str)
    @slot(float, int, result=str)
    def show_value(self, value: float, precison=0) -> str:
        return f'{value * 100:.{precison}f}%'
