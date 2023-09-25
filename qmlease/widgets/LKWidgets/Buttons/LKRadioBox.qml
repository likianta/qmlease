import QtQuick 2.15
import QtQuick.Controls 2.15
import ".."

RadioButton {
    id: root
    height: pysize.bar_height

    property string indicatorBgColor: 'transparent'
    property string indicatorBorderColor: pycolor.border_default
    property string indicatorFgColor: pycolor.text_default
    property bool   showGhostBorder: false

    background: LKRectangle {
        visible: root.showGhostBorder
        border.width: root.hovered ? 1 : 0
        color: 'transparent'
    }

    contentItem: LKText {
        leftPadding: root.indicator.width
        horizontalAlignment: Text.AlignLeft
        verticalAlignment: Text.AlignVCenter
        text: root.text
    }

    indicator: LKRectangle {
        anchors {
            left: parent.left
            verticalCenter: parent.verticalCenter
            margins: 2
        }
        width: radius * 2
        height: radius * 2
        radius: pysize.indicator_radius
        border.width: 1
        border.color: root.checked ?
            root.indicatorFgColor : root.indicatorBorderColor
        clip: true
        color: root.indicatorBgColor

        LKRectangle {
            anchors {
                centerIn: parent
            }
            width: height
            height: root.checked ? parent.height - 4 : 0
            radius: height / 2
            color: root.indicatorFgColor

            Behavior on height {
                NumberAnimation {
                    duration: 200
                    easing.overshoot: 1.5
                    easing.type: Easing.OutBack
                }
            }
        }
    }
}
