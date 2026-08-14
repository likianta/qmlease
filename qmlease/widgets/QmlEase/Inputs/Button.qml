// inspired by daisyui button: https://daisyui.com/components/button/
import QtQuick
import "../Layouts" as L
import "../Other" as O
import "../Visual" as V

Item {
    id: root
    implicitWidth: (
        lpadding +
        (leadingIcon ? _iconSize + _gap : 0) +
        textItem.implicitWidth + 
        (followingIcon ? _gap + _iconSize : 0) +
        rpadding
    )
    implicitHeight: 32

    property string alignment: 'center'
    property string baseColor: pycolor.container
    property bool   bold: false
    property bool   border: false
    property string borderColor: pycolor.outline
    property int    borderWidth: border ? 1 : 0
    property string color: (
        mouse.pressed ?
        pycolor.higher(baseColor, 1) :
        mouse.hovered ?
        pycolor.higher(baseColor, 2) :
        baseColor
    )
    property string followingIcon: ''
    property alias  hovered: mouse.hovered
    property int    hpadding: 24
    property string leadingIcon: ''
    property int    lpadding: hpadding
    property int    rpadding: hpadding
    property string text: ''
    // property string textColor: pycolor.against(color)
    property string textColor: pycolor.on_container
    property int    _gap: 8
    property int    _iconSize: 16

    signal clicked()

    V.Rectangle {
        id: _container
        anchors {
            fill: parent
            margins: mouse.pressed ? 1 : 0
        }
        radius: 8
        border.width: root.borderWidth
        border.color: root.borderColor
        color: root.color
    }

    L.Row {
        x: root.lpadding
        // anchors { horizontalCenter: parent.horizontalCenter }
        y: mouse.pressed ?
            (root.height - height) / 2 + 1 : 
            (root.height - height) / 2
        spacing: root._gap
        valign: 'center'

        V.Icon {
            visible: root.leadingIcon != ''
            size: root._iconSize
            source: root.leadingIcon
            color: root.textColor
        }

        V.Text {
            id: textItem
            // height: parent.height
            // verticalAlignment: Text.AlignVCenter
            text: root.text
            color: root.textColor
            font.bold: root.bold
        }

        V.Icon {
            visible: root.followingIcon != ''
            size: root._iconSize
            source: root.followingIcon
            color: root.textColor
        }
        
        Component.onCompleted: {
            if (root.alignment == 'center') {
                this.anchors.horizontalCenter = parent.horizontalCenter
            } else if (root.alignment == 'end') {
                // TODO
            }
        }
    }

    O.MouseArea {
        id: mouse
        anchors.fill: parent
        onClicked: root.clicked()
    }
}
