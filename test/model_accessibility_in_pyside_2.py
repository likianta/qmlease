# https://chatgpt.com/share/69ba3d6d-8b3c-800a-baf0-467740a07afb
from PySide6.QtCore import (
    QAbstractListModel, 
    QModelIndex,
    QObject, 
    Slot
)
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

class Main(QObject):
    @Slot(QObject)
    def test(self, listview):
        print('before:', listview.property('model'))
        listview.setProperty('model', Model([
            {'name': 'CCC', 'number': 333},
            {'name': 'DDD', 'number': 444},
        ]))
        print('after:', listview.property('model'))

class Model(QAbstractListModel):
    def __init__(self, data):
        super().__init__()
        self._schema = tuple(data[0].keys())
        self._items = data

    def data(self, index: QModelIndex, role: int):
        key = self._schema[role]
        return self._items[index.row()].get(key, '')
    
    def setData(self, index, value, role):
        key = self._schema[role]
        self._items[index.row()][key] = value
        self.dataChanged.emit(index, index)
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._items)
    
    def roleNames(self):
        return {i: k.encode('utf-8') for i, k in enumerate(self._schema)}

app = QApplication([])
engine = QQmlApplicationEngine()
root = engine.rootContext()
main = Main()
root.setContextProperty('main', main)
engine.load('test/model_accessibility_in_pyside_2.qml')
app.exec()
