// inspired by daisyui button: https://daisyui.com/components/button/
import QtQuick
import QmlEase

Item {
    id: root
    implicitWidth: _text.width + 48
    implicitHeight: pysize.button_height

    property alias  border: _container.border
    property string color: pycolor.container
    property string text: ''
    property string textColor: pycolor.text_main
    property string _colorDefault: color
    property string _colorHovered: pycolor.higher(_colorDefault, 2)
    property string _colorPressed: pycolor.higher(_colorDefault, 1)

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
        border.color: pycolor.outline
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
