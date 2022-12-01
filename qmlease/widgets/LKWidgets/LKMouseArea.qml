import QtQuick 2.15

MouseArea {
    id: root
    anchors.fill: parent
    hoverEnabled: true
    property alias hovered: root.containsMouse
}
