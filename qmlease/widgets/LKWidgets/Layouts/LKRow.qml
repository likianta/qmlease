import QtQuick 2.15

Row {
    height: pysize.row_height_m
    spacing: pysize.spacing_m

    property string alignment: 'vcenter'
    //  see [lib:qmlease/qmlside/layout_helper/layout_helper.py
    //      : def auto_align : docstring].
    property bool   autoSize: false
    property bool   stretchHeight: false
    property bool   stretchWidth: false

    Component.onCompleted: {
        if (this.alignment) {
            pylayout.auto_align(this, this.alignment)
        }
        py.qmlease.widget.size_children(this, 'row')
    }
}
