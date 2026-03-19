import QtQuick
import QtQuick.Layouts
import QmlEase

Item {
    id: root
    // implicitWidth: _layout.implicitWidth
    // implicitHeight: _layout.implicitHeight

    default property alias content: _layout.data
    property bool   border: false
    property string borderColor: pycolor.outline_variant
    property string color: pycolor.transparent
    // property bool   horizontal: false
    property int    padding
    property int    spacing: pysize.spacing

    Rectangle {
        anchors.fill: parent
        border.width: root.border ? 1 : 0
        border.color: root.borderColor
        color: root.color
    }

    ColumnLayout {
        id: _layout
        anchors.fill: parent
        anchors.margins: 
            root.padding ? root.padding : (root.border ? pysize.padding_s : 0)
        spacing: root.spacing
    }
}
