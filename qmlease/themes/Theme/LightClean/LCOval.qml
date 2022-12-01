import QtQuick 2.15
import "./LCStyle/dimension.js" as LCGeometry
import "./LCStyle/palette.js" as LCPalette

Rectangle {
    id: root
    implicitWidth: radius * 2
    implicitHeight: radius * 2
    border.width: 0
    border.color: LCPalette.BorderNormal
    color: LCPalette.BgWhite
    radius: LCGeometry.RadiusS

    property alias p_border: root.border
    property alias p_color: root.color
    property alias p_radius: root.radius
}
