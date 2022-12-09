import QtQuick
import LKWidgets

Window {
    visible: true

    Rectangle {
        id: rect1
        objectName: "rect1"
        anchors.fill: parent
        anchors.margins: 12
        color: "lightgray"

        Rectangle {
            id: rect2
            objectName: "rect2"
            color: 'red'
            width: 20
            height: 20

            Behavior on width {
                NumberAnimation {
                    duration: 1000
                }
            }

            Behavior on height {
                NumberAnimation {
                    duration: 1000
                }
            }

//            Component.onCompleted: {
//                this.anchors.horizontalCenter = Qt.binding(
//                    () => rect1.horizontalCenter
//                )
//            }
        }

        Rectangle {
            id: rect3
            x: 20
            y: 20
            color: 'blue'
            width: 10
            height: 10
        }

        LKButton {
            anchors {
                horizontalCenter: parent.horizontalCenter
                bottom: parent.bottom
                margins: 4
            }
            text: 'Changing size'
            onClicked: {
                rect2.width = 30
                rect2.height = 30
            }
        }

        Component.onCompleted: {
//            console.log(Qt)
//            console.log(Qt.binding)
//            rect3.width = Qt.binding(() => rect2.width)
            py.main.simple_add(1, 2)
            py.main.center_it(rect2, rect1)
            py.main.follow_size(rect3, rect2)
        }
    }
}
