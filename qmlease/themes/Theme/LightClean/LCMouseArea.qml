import QtQuick

MouseArea {
    id: root
    anchors.fill: parent
    property alias p_hover_enabled: root.hoverEnabled
    property alias p_hovered: root.containsMouse
}
