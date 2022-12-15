import lk_logger

lk_logger.setup(quiet=True, show_varnames=True)

from lk_utils import xpath

from qmlease import QObject
from qmlease import app
from qmlease import qml_eval
from qmlease import slot


class Main(QObject):
    @slot(object, object)
    def test(self, rect0, rect1):
        qml_eval.bind_anchors_to_parent(rect1, rect0, 'centerIn')


app.register(Main())
app.run(xpath('qml_eval_dynamic_binding.qml'))
