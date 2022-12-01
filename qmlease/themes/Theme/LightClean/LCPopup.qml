import QtQuick 2.15
import QtQuick.Controls 2.15
import "./LCBackground"
import "./LCStyle/dimension.js" as LCDimension
import "./LCStyle/motion.js" as LCMotion
import "./LCStyle/palette.js" as LCPalette

Popup {
    id: root
    width: p_w1; height: p_h1
    x: p_x1; y: p_y1
    closePolicy: Popup.CloseOnEscape  // Allow press esc to close popup
    modal: true  // Forbid user's click event outside the popup window.

    property alias p_closePolicy: root.closePolicy
    //      Popup.CloseOnPressOutside | Popup.CloseOnEscape
    property alias p_delegate: root.contentItem

    // LCMotion.Quick | LCMotion.Soft | LCMotion.Cozy | 1500 (for debug)
    property int p_duration0: LCMotion.Cozy
    property int p_duration1: LCMotion.Quick
    property int __easing0: Easing.OutQuart
    property int __easing1: Easing.OutSine

    property real p_w0: 0;         property real p_w1: 380
    property real p_h0: 0;         property real p_h1: 270
    property real p_x0: 0;         property real p_x1: r_cx
    property real p_y0: 0;         property real p_y1: r_cy
    property real p_opacity0: 0.0; property real p_opacity1: 1.0
    property real r_cx: 0;         property real r_cy: 0

    background: LCRectBg {
        id: _bg
        clip: true
        p_borderless: false
        // p_color: LCPalette.ThemeLightBlue
    }

    contentItem: Item {
        implicitWidth: 200; implicitHeight: 200
        // color: 'yellow'

        Item {  // close button
            id: _close
            anchors.right: parent.right
            anchors.top: parent.top
            width: LCDimension.ButtonCloseWidth
            height: LCDimension.ButtonCloseHeight
            z: 1

            LCText {
                anchors.centerIn: parent
                p_color: LCPalette.ThemeBlue
                p_size: 11
                p_text: "Done"
            }

            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: root.close()
            }
        }
    }

    enter: Transition {
        // 进场动画: 从窗口中心点开始, 宽和高从 0 增加到最终尺寸, 由透明变为不透
        // 明, 动画速度由快到慢, 以强化完成时的动画印象. 透明度动画要比尺寸变化
        // 快一些, 以避免动画拖沓.
        NumberAnimation {
            target: root.contentItem
            property: "opacity"
            duration: p_duration1 / 2
            from: 0; to: 1
        }
        NumberAnimation {
            property: "opacity"
            duration: p_duration0 / 2
            from: p_opacity0; to: p_opacity1
        }
        NumberAnimation {
            property: "width"
            duration: p_duration0
            easing.type: __easing0
            from: p_w0; to: p_w1
        }
        NumberAnimation {
            property: "height"
            duration: p_duration0
            easing.type: __easing0
            from: p_h0; to: p_h1
        }
        NumberAnimation {
            property: "x"
            duration: p_duration0
            easing.type: __easing0
            from: p_x0; to: p_x1
        }
        NumberAnimation {
            property: "y"
            duration: p_duration0
            easing.type: __easing0
            from: p_y0; to: p_y1
        }
    }

    exit: Transition {
        // 不设置 from 属性, 允许用户在动画过程中打断并回退到 inactive 状态.
        NumberAnimation {
            target: root.contentItem
            property: "opacity"
            duration: p_duration1 / 2
            // from: 1
            to: 0
        }
        NumberAnimation {
            property: "opacity"
            duration: p_duration1 / 2
            // from: p_opacity1
            to: p_opacity0
        }
        NumberAnimation {
            property: "width"
            duration: p_duration1
            easing.type: __easing1
            // from: p_w1
            to: p_w0
        }
        NumberAnimation {
            property: "height"
            duration: p_duration1
            easing.type: __easing1
            // from: p_h1
            to: p_h0
        }
        NumberAnimation {
            property: "x"
            duration: p_duration1
            easing.type: __easing1
            // from: p_x1
            to: p_x0
        }
        NumberAnimation {
            property: "y"
            duration: p_duration1
            easing.type: __easing1
            // from: p_y1
            to: p_y0
        }
    }

    Overlay.modal: Rectangle {
        color: "#50000000"
    }

    Component.onCompleted: {
        this.r_cx = Overlay.overlay.width / 2 - p_w1 / 2
        this.r_cy = Overlay.overlay.height / 2  - p_h1 / 2
    }
}
