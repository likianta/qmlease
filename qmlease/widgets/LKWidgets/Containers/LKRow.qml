import QtQuick 2.15

Row {
    height: pysize.row_height_m
    spacing: pysize.spacing_m

    property string alignment: 'vcenter'
    //  see [lib:lk-qtquick-scaffold/qmlside/layout_helper/layout_helper.py
    //      : def auto_align : docstring].
    property bool   autoSize: false

    Component.onCompleted: {
        if (this.alignment) {
            pylayout.auto_align(this, this.alignment)
        }
        if (this.autoSize) {
            pylayout.auto_size_children(this, 'h')
        }
    }
}
