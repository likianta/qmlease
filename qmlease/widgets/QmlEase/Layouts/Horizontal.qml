// a copy of `./Vertical.qml` with subtle modifications.
import QtQuick
import QtQuick.Layouts
import QmlEase

Item {
    id: root
    implicitWidth: _layout.implicitWidth
    implicitHeight: _layout.implicitHeight
    clip: true

    default property alias content: _layout.data
    property alias  border: _border.border
    property string color: pycolor.transparent
    property int    padding
    property bool   placeItemsStart: false
    property int    spacing: pysize.spacing

    Rectangle {
        id: _border
        anchors.fill: parent
        border.color: pycolor.outline_variant
        color: root.color
    }

    RowLayout {
        anchors {
            fill: parent
            margins: root.padding ? 
                root.padding : (root.border ? pysize.padding : 0)
        }
        RowLayout {
            id: _layout
            Layout.fillHeight: true
            spacing: root.spacing
        }
        Empty {
            visible: root.placeItemsStart
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }
}
