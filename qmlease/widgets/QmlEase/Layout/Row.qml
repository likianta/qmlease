import QtQuick

Row {
    width: pysize.wrap
    height: pysize.wrap
    clip: true
    spacing: pysize.spacing_m
    property string alignment: 'vcenter'
    property bool   autoSize: false
    Component.onCompleted: {
        py.qmlease.widget.init_row(this)
    }
}
