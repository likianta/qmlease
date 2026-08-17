import QtQuick
import QmlEase as E

E.Rectangle {
    id: root
    implicitWidth: 240
    radius: 4
    color: pycolor.panel

    property var model

    ListView {
        id: listView
        anchors {
            fill: parent
            topMargin: 24
            bottomMargin: 24
            leftMargin: 8
            rightMargin: 8
        }
        model: root.model
        spacing: 4

        delegate: E.Button {
            width: listView.width
            height: 36
            alignment: 'start'
            bold: ListView.isCurrentItem
            color: (
                ListView.isCurrentItem ? 
                pycolor.paint_brand :
                hovered ?
                pycolor.container_tint :
                root.color
            )
            hpadding: 12
            leadingIcon: model.icon
            text: model.text
            textColor: (
                ListView.isCurrentItem ? 
                pycolor.on_paint_brand :
                hovered ?
                pycolor.on_container_tint :
                pycolor.on_panel
            )
            onClicked: {
                listView.currentIndex = index
            }
        }
    }
}
