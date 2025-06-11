import QtQuick 2.15

Column {
    width: pysize.wrap
    spacing: pysize.spacing_v_m
    property bool autoSize: false
    Component.onCompleted: {
        py.qmlease.widget.size_children(this, 'column')
    }
}
