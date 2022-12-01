import QtQuick 2.15
import ".."

Rectangle {
    id: root
    width: 0
    height: pysize.button_height
    radius: pysize.button_radius
    border.width: pysize.border_width_m
//    border.width: pressed ? 2 : 1
    border.color: hovered ? pycolor.border_active : pycolor.border_default

    property string colorDefault: pycolor.button_bg_default
    property string colorDisabled: pycolor.button_bg_disabled
    property string colorHovered: pycolor.button_bg_hovered
    property string colorPressed: pycolor.button_bg_pressed
    property alias  hovered: _area.containsMouse
    property alias  pressed: _area.pressed
    property string text
    property alias  textDelegate: _text

    signal clicked()

    Behavior on border.color {
        enabled: root.border.width > 0
        ColorAnimation {
            duration: pymotion.duration_m
        }
    }

    Behavior on color {
        ColorAnimation {
            duration: pymotion.duration_s
        }
    }

    LKMouseArea {
        id: _area
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        onClicked: root.clicked()
    }

    LKText {
        id: _text
        anchors.centerIn: parent
        color: root.enabled ? pycolor.text_default : pycolor.text_disabled
        text: root.text
    }

    Component.onCompleted: {
        if (this.width == 0) {
            this.width = Qt.binding(() => {
                return _text.contentWidth * 1.5
            })
        }

        this.color = Qt.binding(() => {
            if (this.enabled) {
                if (this.pressed) {
                    return root.colorPressed
                } else if (this.hovered) {
                    return root.colorHovered
                } else {
                    return root.colorDefault
                }
            } else {
                return root.colorDisabled
            }
        })
    }
}
