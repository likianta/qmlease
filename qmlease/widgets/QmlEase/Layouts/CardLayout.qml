import QtQuick
import "../Layouts" as L
import "../Visual" as V

L.Column {
    id: root
    default property alias content: contentArea.data
    property bool   collapsible: false
    property int    contentPadding: 12
    property string title: ''

    implicitWidth: Math.max(titleText.implicitWidth + 24, 200)
    halign: 'stretch'
    // valign: 'stretch'
    spacing: 0
    border: true
    borderColor: pycolor.outline_thin
    color: pycolor.panel

    V.Rectangle {
        height: 32
        clip: false
        radius: root.borderRadius
        color: pycolor.container

        // gasket
        V.Rectangle {
            anchors.bottom: parent.bottom
            width: parent.width
            height: 8
            clip: false
            radius: 0
            color: parent.color
        }
        
        V.Text {
            id: titleText
            anchors {
                left: parent.left
                leftMargin: 12
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

    // sizing problem: 
    // https://chatgpt.com/share/6a8662e3-8488-83e8-bf0e-cbea4b373f6c
    Item {  // content wrapper
        implicitHeight: 
            (
                contentArea.childrenRect.height > 0 ?
                contentArea.childrenRect.height : 80
            ) + root.contentPadding * 2
        
        Item {  // content area
            id: contentArea
            anchors {
                fill: parent
                margins: root.contentPadding
            }
            // x: parent._padding
            // y: parent._padding
            // implicitWidth: childrenRect.width
            // implicitHeight: childrenRect.height > 0 ? childrenRect.height : 80
        }
    }
}
