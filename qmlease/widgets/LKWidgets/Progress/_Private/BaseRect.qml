import QtQuick 2.0

Rectangle {
    width: pysize.progress_width
    height: pysize.progress_height
    radius: pysize.progress_radius
    color: pycolor.progress_bg

    property real value: 0.0

    Rectangle {
        id: _prog
        width:
        height: parent.height
        radius: parent.radius
    }
}
