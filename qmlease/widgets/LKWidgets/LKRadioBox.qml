import QtQuick

Rectangle {
    id: root
    width: radius * 2
    height: radius * 2
    radius: pysize.indicator_radius

    border.width: checked ? radius * 0.7 : (hovered ? 2 : 1)
    border.color: (checked || hovered) ?
        pycolor.border_active : pycolor.border_inactive
    color: pycolor.white

    property bool hovered: _area.containsMouse
    property bool checked: false
    signal clicked()

    LKMouseArea {
        id: _area
        anchors.fill: parent
        onClicked: {
            root.checked = true
            root.clicked()
        }
    }

    Behavior on border.width {
        NumberAnimation {
            duration: pymotion.duration
//            easing.type: Easing.OutQuad
            easing.type: Easing.OutBack
        }
    }

    Behavior on border.color {
        ColorAnimation {
            duration: pymotion.duration
        }
    }
}
