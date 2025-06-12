import QtQuick 2.15

Row {
    // height: childrenRect.height
    spacing: pysize.spacing_m
    // values: top | bottom | vcenter | vfill
    // deprecate: center | fill
    property string alignment: 'vcenter'
    property bool   autoSize: false
    Component.onCompleted: {
        py.qmlease.widget.init_row(this)
    }
}
