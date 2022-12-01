/// the classic Rectangle-Text-MouseArea structure.
import QtQuick 2.15

LKRectangle {
    id: root

    property bool   hoverEnabled: true
    property alias  hovered: _area.containsMouse
    property string text
    property alias  textDelegate: _text

    signal clicked()

    LKText {
        id: _text
        anchors.centerIn: parent
        text: root.text
    }

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: root.hoverEnabled
        onClicked: root.clicked()
    }
}
