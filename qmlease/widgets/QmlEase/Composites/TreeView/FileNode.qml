import QtQuick
import QtQuick.Layouts
import QmlEase

Rectangle {
    id: root
    width: pysize.entry_width
    height: pysize.entry_height
    border.width: ghostBorder && _area.containsMouse ? 1 : 0
    color: pycolor.transparent

    property bool   checkable
    property bool   checked
    property bool   ghostBorder
    property string name
    property string path

    // signal checkboxClicked()
    signal clicked(string nodeId)

    RowLayout {
        // anchors.fill: parent
        anchors.verticalCenter: parent.verticalCenter
        spacing: pysize.spacing

        CheckBoxIndicator {
            id: _checkbox
            visible: root.checkable
            checked: root.checked
        }

        Text {
            text: root.name
        }
    }

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: true
        onClicked: {
//            if (root.checkable) {
//                root.checkboxClicked()
//            }
            root.clicked(root.path)
        }
    }

    Component.onCompleted: {
        console.log(
            'FileNode',
            this.name,
            this.path,
            this.checked
        )
    }
}
