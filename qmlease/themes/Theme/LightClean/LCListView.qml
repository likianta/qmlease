import QtQuick 2.15
import QtQuick.Controls 2.15
import "./LCStyle/dimension.js" as LCDimension

ListView {
    id: root
    implicitWidth: LCDimension.FlowWidth
    implicitHeight: LCDimension.FlowHeight

    // stop bouncing from scrolling to the start/end.
    boundsBehavior: __scrollable ? Flickable.DragOverBounds : Flickable.StopAtBounds
    clip: true
    // control mouse wheel velocity a little faster than default
    maximumFlickVelocity: 2300
    model: p_model
    spacing: LCDimension.VSpacingXS

    property alias p_currentIndex: root.currentIndex
    property alias p_delegate: root.delegate
    property var   p_model: Array()  // [(str|dict), ...]
    property alias p_scrollWidth: _scroll.width
    property alias p_spacing: root.spacing
    property int   r_count: p_model.length
    property alias r_currentItem: root.currentItem
    property real  r_preferredWidth: root.width - _scroll.width
    property bool  __scrollable: root.contentWidth > root.width

    // show scroll bar
    // https://stackoverflow.com/questions/45650226/qml-attach-scrollbar-to-listview/45651291
    ScrollBar.vertical: ScrollBar {
        id: _scroll
        interactive: __scrollable
    }
}