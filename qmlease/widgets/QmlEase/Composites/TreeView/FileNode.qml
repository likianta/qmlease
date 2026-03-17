import QtQuick
import QtQuick.Layouts
import QmlEase

Item {
    id: root
    width: pysize.entry_width
    height: pysize.entry_height_s

    property bool   checkable
    property bool   checked
    property bool   ghostBorder
    property int    indentation
    property string name
    property string path
    property int    _indicatorSize: 16

    signal clicked(string nodeId)

    function applyCheckStates(value) {
        root.checked = value
    }

    GuideLine {
        visible: root.indentation > 0
        x: 11
        height: root.height
    }

    Rectangle {
        anchors {
            fill: parent
            leftMargin: 25
        }
        border.width: ghostBorder && _area.containsMouse ? 1 : 0
        color: pycolor.transparent

        // signal checkboxClicked()
        signal clicked(string nodeId)

        RowLayout {
            anchors {
                left: parent.left
                // right: parent.right
                verticalCenter: parent.verticalCenter
                margins: 4
            }

            CheckBoxIndicator {
                id: _checkbox
                visible: root.checkable
                width: root._indicatorSize
                height: root._indicatorSize
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
                root.checked = !root.checked
                root.clicked(root.path)
            }
        }
    }
}
