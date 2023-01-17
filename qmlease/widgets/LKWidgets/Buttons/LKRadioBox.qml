import QtQuick 2.15
import QtQuick.Controls 2.15
import ".."

RadioButton {
    id: root
    height: pysize.bar_height

//    QtObject {
//        id: _color_group
//
//        property string checked
//        property string default_
//        property string disabled
//        property string hovered
//        property string pressed
//        property string selected
//
////        Component.onCompleted: {
////            if (!this.checked) {
////                this.checked = Qt.binding(() => this.pressed)
////            }
////        }
//    }

    property string indicatorColorDefault: pycolor.border_default
    property string indicatorColorChecked: pycolor.text_main
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
            top: parent.top
            bottom: parent.bottom
            margins: 2
        }
        width: height
        radius: height / 2
        border.width: 1
        border.color: root.checked ?
            root.indicatorColorChecked :
            root.indicatorColorDefault
        clip: true

        LKRectangle {
            anchors {
                centerIn: parent
            }
            width: height
            height: root.checked ? parent.height - 4 : 0
            radius: height / 2
            color: root.indicatorColorChecked

            Behavior on height {
                NumberAnimation {
                    duration: 200
                    easing.type: Easing.OutBack
                }
            }
        }
    }
}
