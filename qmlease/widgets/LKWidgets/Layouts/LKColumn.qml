import QtQuick 2.15

Column {
    width: pysize.col_width_m
    spacing: pysize.spacing_v_m

    property bool autoSize: false
    property bool stretchHeight: false
    property bool stretchWidth: false

    Component.onCompleted: {
        py.qmlease.widget.size_children(this, 'column')
    }
}
