// inspired by daisyui button: https://daisyui.com/components/button/
import QtQuick
import QmlEase

Item {
    id: root
    implicitWidth: _text.width + 48
    implicitHeight: pysize.button_height

    property alias  border: _container.border
    // the "color seed". if not set, use default colorset.
    property string color
    property string text
    property string textColor: pycolor.on_surface
    property string _colorDefault: color ? color : pycolor.surface_container
    property string _colorHovered: color ? pycolor.derive2(
        pycolor.surface_container, pycolor.surface_container_highest, color
    ) : pycolor.surface_container_highest
    property string _colorPressed: color ? pycolor.derive2(
        pycolor.surface_container_highest, pycolor.surface_container_high, color
    ) : pycolor.surface_container_high

    signal clicked()

    Rectangle {
        id: _container
        anchors {
            fill: parent
            margins: _mouse.pressed ? 1 : 0
        }
        color: (
            _mouse.pressed ? root._colorPressed :
            (_mouse.containsMouse ? root._colorHovered : root._colorDefault)
        )
        border.width: 1
        border.color: pycolor.outline_variant
        // border.color: (
        //     root.color ? py.qmlease.derive_color(
        //         pycolor.outline_variant, 
        //         pycolor.outline_variant, 
        //         pycolor.surface
        //     ) : pycolor.outline_variant
        // )
        radius: pysize.radius_l
    }

    Text {
        id: _text
        anchors { horizontalCenter: parent.horizontalCenter }
        y: _mouse.pressed ?
            (root.height - height) / 2 + 1 : (root.height - height) / 2
        color: root.textColor
        text: root.text
    }

    MouseArea {
        id: _mouse
        anchors.fill: parent
        hoverEnabled: true
        onClicked: root.clicked()
    }
}
