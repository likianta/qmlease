import QtQuick 2.15
import "../LCStyle/motion.js" as LCMotion
import "../LCStyle/palette.js" as LCPalette

LCRectBg {
    id: root
    border.width: 1
    border.color: p_borderless ? root.color : LCPalette.BorderNormal
    color: p_color0
    p_borderless: false

    property bool   p_active: false
    property string p_color0: LCPalette.ButtonNormal
    property string p_color1: LCPalette.ButtonPressed
    // inherits:
    //      property alias p_border
    //      property alias p_borderless
    //      property alias p_radius

    states: [
        State {
            when: p_active
            PropertyChanges {
                target: root
                border.width: 2
                border.color: LCPalette.BorderSink
                color: p_color1
            }
        }
    ]

    transitions: [
        Transition {
            ColorAnimation {
                duration: LCMotion.Swift
                easing.type: Easing.OutQuart
                properties: "color"
            }
        }
    ]
}
