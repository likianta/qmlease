import QtQuick
import QmlEase

Rectangle {
    id: root
    width: target.width
    height: target.height
    border.width: _area.containsMouse ? 1 : 0
    border.color: pycolor.primary
    color: pycolor.transparent

    property Item target

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: true
        propagateComposedEvents: true
        onClicked: py.qmlease.inspect_size(root)
    }
}
