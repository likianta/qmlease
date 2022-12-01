import QtQuick 2.15
import "../LCStyle/dimension.js" as LCDimension
import "../LCStyle/motion.js" as LCMotion
import "../LCStyle/palette.js" as LCPalette

LCRectBg {
    id: root
    implicitWidth: LCDimension.IndicatorCheckWidth
    implicitHeight: LCDimension.IndicatorCheckHeight
    border.width: 1
    border.color: LCPalette.ButtonUnchecked
    clip: true
    color: LCPalette.Transparent
    radius: LCDimension.IndicatorCheckRadius

    property bool p_active: false

    states: [
        State {
            when: p_active
            PropertyChanges {
                target: root
                border.color: LCPalette.ButtonChecked
                color: LCPalette.ButtonChecked
            }
        }
    ]

    transitions: [
        Transition {
            ColorAnimation {
                duration: LCMotion.Swift  // Swift | Soft | Cozy
                easing.type: Easing.OutCubic
                properties: "color"
            }
        }
    ]
}