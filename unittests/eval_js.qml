import QtQuick

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

            Component.onCompleted: {
                this.anchors.horizontalCenter = Qt.binding(
                    () => rect1.horizontalCenter
                )
            }
        }

        Component.onCompleted: {
            py.main.simple_add(1, 2)
            py.main.center_it(rect2, rect1)
        }
    }
}
