import QtQuick
import QtQuick.Controls
import "../Inputs" as I
import "../Visual" as V

Item {
    id: root
    implicitWidth: 120
    implicitHeight: 36
    clip: false // to allow popup to show outside of the parent

    property int    currentIndex: 0
    property string currentText: ''
    property bool   expanded: popup.opened
    property var    model: []

    signal itemAdded(int index, Item item)
    signal selected(int index, string text)

    // function itemAtIndex(index: int) {
    //     return root.model[index]
    // }

    onModelChanged: {
        if (root.model.length > 0) {
            if (root.currentText == '') {
                root.currentText = root.model[0]
            }
        }
    }

    I.Button {
        id: display
        anchors.fill: parent
        alignment: 'start'
        hpadding: 20
        border: true
        text: root.currentText

        onClicked: {
            if (root.expanded) {
                popup.close()
            } else {
                popup.open()
            }
        }
        
        V.Icon {
            anchors {
                right: parent.right
                rightMargin: 8
                // verticalCenter: parent.verticalCenter
            }
            y: parent.textYPosition
            source: '../Resources/caret-left.svg'
            color: pycolor.text_secondary
            rotation: root.expanded ? -90 : 0

            Behavior on rotation {
                NumberAnimation {
                    duration: 50
                }
            }
        }
    }

    Popup {
        id: popup
        x: 0
        y: display.height + 4
        width: root.width
        height: _preferredContentHeight + topPadding + bottomPadding
        padding: 4
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent

        property int _entryHeight: 32
        property int _preferredContentHeight: 
            root.model.length == 0 ? 
            _entryHeight :
            root.model.length > 20 ?
            _entryHeight * 20 + _spacing * 19 :
            _entryHeight * root.model.length +
            _spacing * (root.model.length - 1)
        property int _spacing: 4

        background: V.Rectangle {
            border.width: 1
            color: pycolor.panel
            radius: 8
        }

        contentItem: ListView {
            // popup's background and contentItem should not define their own
            // explicit size. they are auto calculated when popup size changes.
            id: listView
            clip: true
            model: root.model
            spacing: popup._spacing

            property int _entryHeight: 32

            // ref: ../Layouts/Sidebar.qml
            delegate: I.Button {
                width: listView.width
                height: popup._entryHeight
                alignment: 'start'
                hpadding: 16

                bold: ListView.isCurrentItem
                color: (
                    ListView.isCurrentItem ?
                    pycolor.paint_brand :
                    hovered ?
                    pycolor.container_tint :
                    pycolor.panel
                )
                text: typeof modelData === "string" ?
                    modelData : modelData.label
                textColor: (
                    ListView.isCurrentItem ? 
                    pycolor.on_paint_brand :
                    hovered ?
                    pycolor.on_container_tint :
                    pycolor.on_panel
                )

                property bool selected: ListView.isCurrentItem

                onClicked: {
                    listView.currentIndex = index
                    root.currentIndex = index
                    root.currentText = this.text
                    root.selected(index, this.text)
                    popup.close()
                }
                
                Component.onCompleted: {
                    root.itemAdded(index, this)
                }
            }

            // Component.onCompleted: {
            //     pylayout.inspect_size(root, 'SelectBox:root')
            //     pylayout.inspect_size(popup, 'SelectBox:popup')
            //     pylayout.inspect_size(listView, 'SelectBox:listView')
            // }
        }
    }
}
