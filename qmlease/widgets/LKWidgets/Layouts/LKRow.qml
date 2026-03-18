import QtQuick 2.15

Row {
    width: pysize.wrap
    height: pysize.wrap
    // height: childrenRect.height
    clip: true
    spacing: pysize.spacing_m
    // values: top | bottom | vcenter | vfill
    // deprecate: center | fill

    property string alignment: 'vcenter'
    property bool   autoSize: false

//    function resize() {
//        py.qmlease.resize_row(this)
//    }

    Component.onCompleted: {
        py.qmlease.init_row(this)
    }
}
