from lk_utils import xpath

from qmlease import QObject
from qmlease import app
from qmlease import slot


class MyObject(QObject):
    @slot()
    def test(self):
        print('hello world')


app.register(MyObject, 'MyObject', 'dev.likianta.qmlease')
app.run(xpath('pyside2_register_pyclass.qml'))
