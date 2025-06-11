import QtQuick 2.15

Column {
    width: childrenRect.width
    spacing: pysize.spacing_v_m
    property bool autoSize: false
    Component.onCompleted: {
        py.qmlease.widget.size_children(this, 'column')
    }
}
