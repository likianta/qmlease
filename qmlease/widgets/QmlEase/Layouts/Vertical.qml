import QtQuick
import QtQuick.Layouts
import QmlEase

Item {
    id: root
    implicitWidth: _layout.implicitWidth
    implicitHeight: _layout.implicitHeight
    // width: _layout.width
    // height: _layout.height
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

    // here is an incorrect answer by chatgpt, but recommend reading:
    //  https://chatgpt.com/share/69c1f13a-6b4c-800a-9221-76559090f735
    ColumnLayout {
        anchors {
            fill: parent
            margins: root.padding ? 
                root.padding : (root.border ? pysize.padding : 0)
        }

        ColumnLayout {
            id: _layout
            Layout.fillWidth: true
            // Layout.fillHeight: true
            spacing: root.spacing
        }

        Empty {
            visible: root.placeItemsStart
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }
}
