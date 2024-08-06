/// a rectangle with mouse hover enabled.
import QtQuick 2.15

Rectangle {
    border.color:
        mousePressed ? borderColor2 :
        (mouseEntered ? borderColor1 : borderColor0)
    color: mousePressed ? color2 : (mouseEntered ? color1 : color0)
    radius: pysize.radius_m

    property string borderColor0: pycolor.border_default
    property string borderColor1: pycolor.border_active
    property string borderColor2: borderColor1
    property string color0: pycolor.button_bg_default
    property string color1: pycolor.button_bg_hovered
    property string color2: color1
    property alias  mouseArea: _area
    property alias  mouseEntered: _area.containsMouse
    property alias  mousePressed: _area.pressed

    signal clicked()

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: true
        onClicked: parent.clicked()
    }
}
