// inspired by daisyui button: https://daisyui.com/components/button/
import QtQuick
import QmlEase as E

Item {
    id: root
    implicitWidth: (
        lpadding +
        (leading_icon ? _icon_size + _gap : 0) +
        textItem.implicitWidth + 
        (following_icon ? _gap + _icon_size : 0) +
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
    property string following_icon: ''
    property alias  hovered: mouse.hovered
    property int    hpadding: 12
    property string leading_icon: ''
    property int    lpadding: hpadding
    property int    rpadding: hpadding
    property string text: ''
    property string textColor: pycolor.against(color)
    property int    _gap: 4
    property int    _icon_size: 16

    signal clicked()

    E.Rectangle {
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

    E.Row {
        x: root.lpadding
        // anchors { horizontalCenter: parent.horizontalCenter }
        y: mouse.pressed ?
            (root.height - height) / 2 + 1 : 
            (root.height - height) / 2
        spacing: root._gap

        E.Icon {
            visible: root.leading_icon != ''
            anchors.verticalCenter: parent.verticalCenter
            size: root._icon_size
            source: root.leading_icon
            color: root.textColor
        }

        E.Text {
            id: textItem
            height: parent.height
            verticalAlignment: Text.AlignVCenter
            text: root.text
            color: root.textColor
            font.bold: root.bold
        }

        E.Icon {
            visible: root.following_icon != ''
            anchors.verticalCenter: parent.verticalCenter
            size: root._icon_size
            source: root.following_icon
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

    E.MouseArea {
        id: mouse
        anchors.fill: parent
        onClicked: root.clicked()
    }
}
