import QtQuick
Rectangle {
    width: horizontal ? parent.width : 1
    height: horizontal ? 1 : parent.height
    color: pycolor.outline
    property bool horizontal: true
}