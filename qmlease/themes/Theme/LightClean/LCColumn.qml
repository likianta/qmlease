import QtQuick
import "./LCStyle/dimension.js" as LCDimension

Column {
    id: root
    padding: LCDimension.Padding
    spacing: LCDimension.VSpacingM

    property bool p_align_center: false
    property bool p_elastic_layout: true
    property bool p_fill_width: true

    Component.onCompleted: {
        if (p_align_center) { LKLayoutHelper.valign_center(root) }
        if (p_elastic_layout) { LKLayoutHelper.vadjust_children_size(root) }
        if (p_fill_width) { LKLayoutHelper.fill_width(root) }
    }
}
