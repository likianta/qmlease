// NOTE: this component doesn't expose to qmldir.
// DELETE: depreciated to use and going to be removed since 2020-12-01.

import QtQuick 2.15
import QtQuick.Controls 2.15

import "../"
import "../LCStyle/dimension.js" as LCDimension
import "../LCStyle/palette.js" as LCPalette
import "../LCStyle/typography.js" as LCText

Button {
    id: root
    implicitWidth: LCDimension.ButtonWidthM
    implicitHeight: LCDimension.ButtonHeightM

    property bool   p_active: false
    //      p_active best practices:
    //          1. `p_active: root.pressed`
    //          2. `onPressed: p_active = !p_active`
    //          3. `RadioButton { delegate: LCBaseButton { p_active: checked } }`
    property bool   p_autoSize: true
    property alias  p_border: _bg.p_border
    //      you can set `p_border.width: 0` to make button frameless.
    property string p_colorBg0: LCpalette.BgWhite
    property string p_colorBg1: LCpalette.BgWhite
    property string p_colorText0: LCPalette.TextNormal
    property string p_colorText1: LCPalette.TextNormal
    property alias  p_text: root.text
    property alias  __bg: _bg
    property alias  __txt: _txt

    background: LCRectangleBg {
        id: _bg
        p_active: root.p_active
        p_border.color: LCPalette.BorderNormal
        p_color0: p_colorBg0; p_color1: p_colorBg1
    }

    contentItem: Item {
        LCText {
            id: _txt
            anchors.centerIn: parent
            p_bold: true
            p_color: p_active ? p_colorText1 : p_colorText0
            p_size: LCText.ButtonTextSize
            p_text: root.text
        }
    }

    Component.onCompleted: {
        if (p_autoSize) {
            const preferredWidth = _txt.contentWidth + LCDimension.PaddingM * 2
            if (preferredWidth > p_width) {
                this.width = preferredWidth
            }
        }
    }
}
