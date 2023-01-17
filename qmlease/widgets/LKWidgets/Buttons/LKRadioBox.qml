import QtQuick 2.15
import QtQuick.Controls 2.15
import ".."

RadioButton {
    id: root
    height: pysize.bar_height

//    property var  model  // list[str]
    property bool showGhostBorder: false

    background: LKRectangle {
        visible: root.showGhostBorder
        border.width: root.hovered ? 1 : 0
        color: 'transparent'
    }

    indicator: LKRectangle {
        anchors {
            left: parent.left
            top: parent.top
            bottom: parent.bottom
            margins: 4
        }
        width: height
        radius: height / 2
        border.width: 1

        LKRectangle {
            anchors {
                fill: parent
                margins: 3
            }
            color: 'black'
            radius: height / 2
            visible: root.checked
        }
    }
}
