import QtQuick 2.15
import QtQuick.Controls 2.15
import "./LCBackground"
import "./LCButtons"
import "./LCStyle/dimension.js" as LCDimension
import "./LCStyle/palette.js" as LCPalette

Button {
    id: root
    implicitWidth: _txt.implicitWidth + _txt.leftPadding + _txt.rightPadding
    implicitHeight: _txt.implicitHeight + _txt.topPadding + _txt.bottomPadding
    flat: true
    hoverEnabled: true

    property alias  p_text: root.text
    property alias  __active: root.pressed

    background: LCRectBg {
        id: _bg
        p_color: LCPalette.ThemeLightBlue
        p_radius: implicitBackgroundHeight / 2
    }

    contentItem: LCText {
        id: _txt
        leftPadding: LCDimension.PaddingM
        rightPadding: LCDimension.PaddingM
        topPadding: LCDimension.VSpacingXS
        bottomPadding: LCDimension.VSpacingXS

        p_alignment: 'lcenter'
        p_bold: true
        p_color: LCPalette.TextLink
        p_text: root.text

        states: [
            State {
                // When hovered, show underline to text
                when: root.hovered
                PropertyChanges {
                    target: _txt
                    p_text: '<u>' + root.text + '</u>'
                }
            }
        ]

        // transitions: [
        //     Transition {
        //         NumberAnimation {
        //             duration: 1000
        //             properties: 'opacity'
        //         }
        //     }
        // ]
    }
}

