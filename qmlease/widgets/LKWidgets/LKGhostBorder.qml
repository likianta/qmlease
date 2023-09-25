import QtQuick 2.15

LKRectangle {
    width: pysize.bar_width
    height: pysize.bar_height
    border.width: _area.containsMouse ? 1 : 0
    border.color: pycolor.border_default
    color: 'transparent'
    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: true
    }
}
