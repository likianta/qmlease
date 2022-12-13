from lk_utils import xpath

from qmlease import QObject
from qmlease import app
from qmlease import eval_js
from qmlease import slot


class Main(QObject):
    @slot(object)
    def test(self, obj: QObject):
        eval_js('''
            console.log(obj.objectName)
            const a = 1 / 0
            console.log(a)
            obj.nonexistent_method()
        ''', {'obj': obj})


app.register(Main())
app.run(xpath('eval_js_panic.qml'))
