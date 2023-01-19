import QtQuick 2.15

Item {
    id: root
    property string color: pycolor.progress_fg
    property int    radius: pysize.progress_radius
    property real   value: 0  // 0.0 ~ 1.0
    Rectangle {
        id: _rect
        width: parent.width * parent.value
        height: parent.height
        radius: parent.radius
        color: parent.color
    }
}
