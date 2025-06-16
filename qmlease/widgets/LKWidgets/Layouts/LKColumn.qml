import QtQuick 2.15

Column {
    width: pysize.wrap
    height: pysize.wrap
//    width: childrenRect.width
//    height: childrenRect.height
    clip: true
    spacing: pysize.spacing_v_m
    // values: left | right | hcenter | hfill
    // deprecate: center | fill
    property string alignment: 'left'
//    property string alignment: 'hfill'
    property bool   autoSize: false
    Component.onCompleted: {
        py.qmlease.widget.init_column(this)
    }
}
