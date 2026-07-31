// a copy of `./Vertical.qml` with subtle modifications.
import QtQuick
import QtQuick.Layouts
import QmlEase

Item {
    id: root
    implicitWidth: _layout.implicitWidth + _implicitPadding * 2
    implicitHeight: _layout.implicitHeight + _implicitPadding * 2
    clip: true

    default property alias content: _layout.data
    property alias  border: _border.border
    property string color: pycolor.transparent
    property int    padding
    property bool   placeItemsStart: false
    property bool   showBorder: false
    property int    spacing: pysize.spacing
    property int    _implicitPadding: (
        padding ? padding : (showBorder ? pysize.padding : 0)
    )

    Rectangle {
        id: _border
        anchors.fill: parent
        border.width: root.showBorder ? 1 : 0
        border.color: pycolor.outline
        color: root.color
    }

    RowLayout {
        anchors {
            fill: parent
            margins: _implicitPadding
        }
        RowLayout {
            id: _layout
            Layout.fillHeight: true
            spacing: root.spacing
        }
        Empty {
            visible: root.placeItemsStart
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }
}
