// inspired by daisyui button: https://daisyui.com/components/button/
import QtQuick
import QmlEase

Item {
    id: root
    implicitWidth: _text.width + 48
    implicitHeight: _text.height + 16

    property string text

    signal clicked()

    Rectangle {
        anchors {
            fill: parent
            margins: _mouse.pressed ? 1 : 0
        }
        color: (
            _mouse.pressed ? pycolor.surface_container_high :
            (
                _mouse.containsMouse ?
                pycolor.surface_container_highest : pycolor.surface_container
            )
        )
        border.width: 1
        border.color: pycolor.outline_variant
        radius: pysize.radius_l
    }

    Text {
        id: _text
        anchors { horizontalCenter: parent.horizontalCenter }
        y: _mouse.pressed ?
            (root.height - height) / 2 + 1 : (root.height - height) / 2
        color: pycolor.on_surface
        text: root.text
    }

    MouseArea {
        id: _mouse
        anchors.fill: parent
        hoverEnabled: true
        onClicked: root.clicked()
    }
}
