import QtQuick 2.15
import QtQuick.Controls 2.15
import "../"
import "../LCStyle/dimension.js" as LCGeometry
import "../LCStyle/palette.js" as LCPalette

RadioButton {
    id: _root
    hoverEnabled: true

    // p_colorBg0: LCPalette.Transparent
    // p_colorBg1: LCPalette.Transparent
    property alias p_text: _txt.p_text
    property alias __active: _root.checked

    background: LCRectangleBg {
        id: _bg
        color: {
            if (_root.hovered) {
                return LCPalette.ButtonHovered
            } else if (_root.pressed) {
                return LCPalette.ButtonPressed
            } else {
                return LCPalette.Transparent
            }
        }
        implicitWidth: LCGeometry.ButtonWidthM; implicitHeight: LCGeometry.ButtonHeightM

        // p_active: __active
        p_border.width: 0
        // p_color0: _root.p_colorBg0
        // p_color1: _root.p_colorBg1
    }
    contentItem: LCText {
        id: _txt
        anchors.fill: parent
        anchors.leftMargin: LCGeometry.HSpacingS
        p_alignment: "vcenter"
        p_bold: false
        p_color: __active ? LCPalette.TextHighlight : LCPalette.TextNormal
    }
    indicator: Item {}
}