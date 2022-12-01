import QtQuick 2.15

Column {
    width: pysize.col_width_m
    spacing: pysize.spacing_v_m

    property string alignment: 'hcenter'
    //  warning: if child type is Repeater, the `alignment` cannot work.
    property bool   autoSize: false

    Component.onCompleted: {
        if (this.alignment) {
            pylayout.auto_align(this, this.alignment)
        }
        if (this.autoSize) {
            pylayout.auto_size_children(this, 'v')
        }
    }
}
