import QtQuick
import QtQuick as Q
import QmlEase

Item {
    default property alias content: _column.data
    property bool   border: false
    property bool   borderColor: pycolor.outline
    property string color: pycolor.surface
    property int    spacing: pysize.spacing_s

    Rectangle {
        anchors.fill: parent
        border.width: parent.border ? 1 : 0
        border.color: parent.borderColor
        color: parent.color
    }

    Q.Column {
        id: _column
        anchors.fill: parent
        clip: true
        spacing: parent.spacing
    }
}
