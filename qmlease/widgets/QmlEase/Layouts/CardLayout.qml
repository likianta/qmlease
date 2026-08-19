import QtQuick
import "../Layouts" as L
import "../Visual" as V

L.Column {
    id: root

    default property alias content: contentContainer.data
    property bool   collapsible: false
    property string title: ''

    halign: 'stretch'
    valign: 'stretch'
    spacing: 0
    color: pycolor.panel

    V.Rectangle {
        width: parent.width
        height: 32
        color: pycolor.container
        radius: parent.borderRadius

        // gasket
        V.Rectangle {
            anchors.bottom: parent.bottom
            width: parent.width
            height: 8
            border.radius: 0
            color: parent.color
        }
        
        V.Text {
            anchors {
                left: parent.left
                margins: 12
                verticalCenter: parent.verticalCenter
            }
            text: root.title
            color: pycolor.text_secondary
            font.bold: true
        }
    }

    V.DividerLine {
        horizontal: true
        thin: true
    }

    Item {
        property int _stretch: 1
        Item {
            id: contentContainer
            anchors {
                fill: parent
                margins: 12
            }
        }
    }
}
