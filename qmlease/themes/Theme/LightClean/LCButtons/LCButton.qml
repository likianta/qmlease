import QtQuick 2.15
import QtQuick.Controls 2.15

import "../"
import "../LCBackground"
import "../LCStyle/dimension.js" as LCDimension
import "../LCStyle/palette.js" as LCPalette
import "../LCStyle/typography.js" as LCTypo

Button {
    id: root
    implicitWidth: LCDimension.ButtonWidthM
    implicitHeight: LCDimension.ButtonHeightM
    
    property bool   p_autoWidth: true
    property alias  p_borderless: _bg.p_borderless
    property alias  p_enabled: root.enabled
    property alias  p_text: root.text
    property alias  p_textColor: _txt.p_color
    property alias  __active: root.pressed
    property alias  __textComp: _txt  // Access this only for special intent.
    
    background: LCButtonBg {
        id: _bg
        p_active: __active
    }

    contentItem: LCText {
        id: _txt
        // anchors.centerIn: parent
        p_bold: true
        p_size: LCTypo.ButtonTextSize
        p_text: root.text

        states: State {
            when: !root.p_enabled
            PropertyChanges {
                target: _txt
                p_color: LCPalette.TextDisabled
            }
        }
    }

    Component.onCompleted: {
        if (p_autoWidth) {
            const preferredWidth = _txt.contentWidth + 40
            if (preferredWidth > root.implicitWidth) {
                root.width = preferredWidth
            }
        }
    }
}
