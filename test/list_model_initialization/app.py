from qtpy.QtCore import (
    QAbstractListModel,
    QModelIndex,
    QByteArray,
    QObject,
    Qt,
    Slot,
)
from qtpy.QtQml import QQmlApplicationEngine
from qtpy.QtWidgets import QApplication
from lk_utils import fs


class SidebarModel(QAbstractListModel):
    IconRole = Qt.UserRole + 1
    TextRole = Qt.UserRole + 2

    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        self._items = items or []

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._items)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        item = self._items[index.row()]

        if role == self.IconRole:
            return item['icon']
        if role == self.TextRole:
            return item['text']

        return None

    def roleNames(self):
        return {
            self.IconRole: QByteArray(b'icon'),
            self.TextRole: QByteArray(b'text'),
        }


class Sidebar(QObject):
    @Slot(result='QVariant')
    def init_model(self):
        return SidebarModel(
            [
                {'icon': 'icons/home.svg', 'text': 'Home'},
                {'icon': 'icons/settings.svg', 'text': 'Settings'},
                {'icon': 'icons/about.svg', 'text': 'About'},
            ]
        )

    @Slot(QObject)
    def init_model_2(self, qobj):
        qobj.setProperty(
            'model',
            SidebarModel(
                [
                    {'icon': 'icons/home.svg', 'text': 'Home'},
                    {'icon': 'icons/settings.svg', 'text': 'Settings'},
                    {'icon': 'icons/about.svg', 'text': 'About'},
                ]
            ),
        )


app = QApplication([])
engine = QQmlApplicationEngine()

sidebar = Sidebar()
engine.rootContext().setContextProperty('sidebar', sidebar)

engine.load('file:///' + fs.here('view.qml'))
app.exec()
