import QtQuick
import LKWidgets

Item {
//    LKColumn {
//        id: col
//        property int a: Flow.LeftToRight
//        property int b: Flow.TopToBottom
//        LKRow {
//            width: 100
//            height: 100
//        }
//    }
    Flow {
        id: myflow
        property int plainFlow: flow == Flow.LeftToRight ? 0 : 1
    }
    LKButton {
        text: 'Test'
        onClicked: py.inspector.inspect(myflow)
    }
}
