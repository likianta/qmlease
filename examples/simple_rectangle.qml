// run: qmlease run examples/simple_rectangle.qml
import QtQuick
import QmlEase

Window {
    Rectangle {
        anchors.centerIn: parent
        width: 120
        height: 120
        
        color: mouse.hovered ? pycolor.paint_brand : pycolor.paint_error

        Behavior on color {
            ColorAnimation {
                duration: 200
            }
        }

        MouseArea {
            id: mouse
            anchors.fill: parent
        }
    }
}