import qmlease as qe
from lk_utils import fs
from neoprint import print


class TestFramework(qe.QObject):
    @qe.Slot(object)
    def test_ui(self, window: qe.QObject) -> None:
        print(':d', 'TEST UI START')

        btn = window.find_child('testButton')
        assert btn is not None
        qe.layout.inspect_size(btn)
        btn.clicked.emit()

        print(':t', 'TEST UI END')
        qe.app.force_exit()


qe.app.register(TestFramework)
qe.app.run(fs.here('debug_running_app.qml'))
