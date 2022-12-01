import QtQuick 2.15
import "../LCStyle/dimension.js" as LCDimension
import "../LCStyle/palette.js" as LCPalette

Rectangle {
    id: root
    implicitWidth: LCDimension.BarWidth
    implicitHeight: LCDimension.BarHeight

    border.width: p_borderless ? 0 : 1
    border.color: LCPalette.BorderNormal
    color: LCPalette.BgWhite
    radius: LCDimension.RadiusM

    property alias p_border: root.border
    property bool  p_borderless: true
    property alias p_color: root.color
    property alias p_radius: root.radius
}
