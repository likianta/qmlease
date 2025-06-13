import QtQuick 2.15
import ".."

Rectangle {
    id: root
    width: _text.contentWidth * 1.5
    // width: py.qmlease.widget.estimate_line_width(text) + pysize.padding * 2
    height: pysize.button_height
    radius: pysize.button_radius
    border.width: pysize.border_width_m
//    border.width: pressed ? 2 : 1
    border.color: hovered ? pycolor.border_active : pycolor.border_default
    clip: true

    readonly property alias textItem: _text
    readonly property alias hovered: _area.containsMouse
    readonly property alias pressed: _area.pressed

    property string bgColor: pycolor.button_bg_default
    property alias  bgColorDefault: root.bgColor
    property string bgColorDisabled: pycolor.button_bg_disabled
    property string bgColorHovered: pycolor.button_bg_hovered
    property string bgColorPressed: pycolor.button_bg_pressed
//    property alias  borderColor: root.border.color
    property alias  text: _text.text
    property string textColor: pycolor.text_default

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
        // anchors.centerIn: parent
        anchors.fill: parent
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        color: root.enabled ? root.textColor : pycolor.text_disabled
    }

    Component.onCompleted: {
        this.color = Qt.binding(() => {
            if (this.enabled) {
                if (this.pressed) {
                    return root.bgColorPressed
                } else if (this.hovered) {
                    return root.bgColorHovered
                } else {
                    return root.bgColor
                }
            } else {
                return root.bgColorDisabled
            }
        })
    }
}
