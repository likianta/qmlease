import QtQuick 2.15
import ".."

Item {
    id: root
    width: pysize.panel_width
    height: pysize.panel_height

    property alias     border: _frame.border
    property string    color: pycolor.panel_bg
    property Component delegate
    property alias     textColor: _text.color
    property string    title
    property alias     __titleHeight: _text.height

    LKRectangle {
        id: _frame
        anchors.fill: parent
        anchors.topMargin: root.__titleHeight / 2
        border.width: 1
        border.color: pycolor.border_default
        color: root.color

        property string title

        Loader {
            anchors.fill: parent
            anchors.topMargin: root.__titleHeight / 2
            clip: true
            sourceComponent: root.delegate
        }
    }

    Rectangle {
        id: _title
        x: 8
        visible: Boolean(root.title)
        width: _text.width + pysize.padding_m * 2
        height: _text.height
        radius: _frame.radius
        color: _frame.color

        LKText {
            id: _text
            anchors.centerIn: parent
            text: root.title
        }
    }
}
