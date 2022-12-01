import QtQuick 2.15
import "LKProgress"

LKProgress {
    id: root
    width: pysize.bar_width
    height: pysize.bar_height
    demoMode: false
    showText: true

    signal progressChangedByUser(real value)

    Item {
        id: _invisible_draggee
    }

    MouseArea {
        anchors.fill: parent
        drag.target: _invisible_draggee

//        property real __progWidth: root.progItem.width

        function __updateProgress(x) {
            root.progValue = x / root.progItem.width
            root.progressChangedByUser(root.__progValue)
        }

        onClicked: (mouse) => {
            __updateProgress(mouse.x)
        }

        onPositionChanged: (mouse) => {
            if (this.drag.active) {
                __updateProgress(mouse.x)
            }
        }

//        Component.onCompleted: {
//            this.__progWidth = Qt.binding(() => root.progItem.width)
//        }
    }
}
