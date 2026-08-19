import QtQuick

Rectangle {
    property bool horizontal: true
    property bool thin: false
    width: horizontal ? parent.width : 1
    height: horizontal ? 1 : parent.height
    color: thin ? pycolor.outline_thin : pycolor.outline
}