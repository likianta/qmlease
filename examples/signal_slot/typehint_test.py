from PySide6.QtCore import QObject, Signal, Slot
from qmlease import signal, slot  # requires v2.0.0+


class SignalTest(QObject):
    aaa_changed = Signal(int, str)
    bbb_changed = signal(int, str)
    
    def test_connect(self):
        self.aaa_changed.connect(self.bar)
        self.bbb_changed.connect(self.bar)
    
    def foo(self):
        self.aaa_changed.emit(1, 'aaa')
        self.bbb_changed.emit(2, 'bbb')
    
    @Slot(int, str, result=bool)
    def bar(self, index: int, text: str) -> bool:
        print('bar', index, text)
        return True
    
    @slot(int, str, result=bool)
    def bar(self, index: int, text: str) -> bool:
        print('bar', index, text)
        return False
