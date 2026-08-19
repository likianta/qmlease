import qmlease as qe
from lk_utils import fs
from neoprint import print
from qtpy.QtCore import QTimer


class Main(qe.QObject):
    @qe.Slot(object)
    def test_ui(self, window: qe.QObject) -> None:
        print(':d', 'test ui started')

        btn = window.find_child('testButton')
        assert btn is not None
        qe.layout.inspect_size(btn)
        btn.clicked.emit()

        print(':t', 'over')
        # qe.app.quit()
        QTimer.singleShot(0, qe.app.quit)


qe.app.register(Main)
qe.app.run(fs.here('view.qml'))
