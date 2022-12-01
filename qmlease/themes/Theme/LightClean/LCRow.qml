import QtQuick
import "./LCStyle/dimension.js" as LCDimension

Row {
    id: root
    padding: LCDimension.Padding
    spacing: LCDimension.HSpacingM

    property bool p_align_center: false
    property bool p_elastic_layout: true
    property bool p_fill_height: false

    Component.onCompleted: {
        if (p_align_center) { LKLayoutHelper.halign_center(root) }
        if (p_elastic_layout) { LKLayoutHelper.hadjust_children_size(root) }
        if (p_fill_height) { LKLayoutHelper.fill_height(root) }
    }
}
