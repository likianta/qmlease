import QtQuick 2.15
import QtQuick.Controls 2.15

DropArea {
    property string maskColor: pycolor.button_bg_hovered
    property bool   showMask: true

    signal fileDropped(string path)

    onDropped: (event) => {
        if (event.hasUrls) {
            this.fileDropped(lkutil.normalize_path(event.text))
        }
    }

    LKRectangle {
        visible: parent.showMask
        anchors.fill: parent
        color: parent.maskColor
        border.width: 1
        border.color: pycolor.border_active
        opacity: parent.containsDrag ? 0.5 : 0
        Behavior on opacity {
            NumberAnimation {
                duration: 100
            }
        }
    }
}
