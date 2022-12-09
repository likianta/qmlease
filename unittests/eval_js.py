from lk_utils import xpath

from qmlease import QObject
from qmlease import app
from qmlease import eval_js
from qmlease import qlogger
from qmlease import slot

qlogger.SHOW_FUNCNAME = True


class Main(QObject):
    
    @slot(int, int)
    def simple_add(self, a: int, b: int):
        print(eval_js('return a + b', {'a': a, 'b': b}))
        print(eval_js('console.log(a + b)', {'a': a, 'b': b}))
        print(eval_js('''
            console.log(a + b)
            return a + b
        ''', {'a': a, 'b': b}))
    
    @slot(object, object)
    def center_it(self, child: QObject, parent: QObject) -> None:
        eval_js('''
            console.log('center it')
            console.log(child, parent)
            console.log(child.objectName, parent.objectName)
            console.log(Qt)
            console.log(Qt.LeftButton)
            console.log(Qt.binding)
            // child.anchors.right = Qt.binding(() => parent.right)
            // child.anchors.bottom = Qt.binding(() => parent.bottom)
            child.anchors.bottom = parent.bottom
            // child.anchors.right = parent.right
            // child.anchors.bottom = parent.bottom
            child.width = 40
            child.height = 40
            // child.anchors.centerIn = Qt.binding(() => parent)
            // child.anchors.centerIn = parent
            // child.anchors.horizontalCenter = Qt.binding(
            //     () => parent.horizontalCenter
            // )
        ''', {'child': child, 'parent': parent})


app.register(Main())
app.run(xpath('eval_js.qml'))
