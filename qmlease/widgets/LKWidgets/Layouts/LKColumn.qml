import QtQuick 2.15

Column {
    // width: childrenRect.width
    spacing: pysize.spacing_v_m
    // values: left | right | hcenter | hfill
    // deprecate: center | fill
    property string alignment: 'left'
    property bool   autoSize: false
    Component.onCompleted: {
        py.qmlease.widget.init_column(this)
    }
}
