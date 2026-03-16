import QtQuick
import QtQuick.Layouts
import QmlEase

ColumnLayout {
    id: root

    default property alias content: _stack.data
    // default property alias content: _swipe.contentData
    property int index
    property var model  // arrray of strings

    ColumnLayout {
        Layout.fillWidth: true

        RowLayout {
            spacing: pysize.spacing_s

            Repeater {
                id: _titleTabs
                model: root.model
                delegate: Rectangle {
                    width: _tabText.width + 24 * 2
                    height: pysize.entry_height_s
                    color: _tabArea.containsMouse ?
                        pycolor.surface_container : pycolor.transparent

                    property bool selected: model.index == root.index

                    Text {
                        id: _tabText
                        anchors.centerIn: parent
                        font.bold: parent.selected
                        text: modelData
                    }

                    MouseArea {
                        id: _tabArea
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: root.index = model.index
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 2
            color: pycolor.surface_container  // full-width divider line (grey)

            Rectangle {
                id: _tabsIndicator
                // x: _titleTabs.itemAt(root.index).x
                // width: _titleTabs.itemAt(root.index).width
                width: 0
                height: parent.height + 1
                color: pycolor.theme_blue

                function initAxisBinding() {
                    this.x = Qt.binding(
                        () => _titleTabs.itemAt(root.index).x
                    )
                    this.width = Qt.binding(
                        () => _titleTabs.itemAt(root.index).width
                    )
                }

                Behavior on x {
                    NumberAnimation {
                        duration: 150
                        easing.type: Easing.OutCubic
                    }
                }
            }
        }
    }

//    SwipeView {
//        id: _swipe
//        Layout.fillWidth: true
//        Layout.fillHeight: true
//        clip: true
//        currentIndex: root.index
//        interactive: false
//    }
    StackLayout {
        id: _stack
        Layout.fillWidth: true
        Layout.fillHeight: true
        clip: true
        currentIndex: root.index
    }

    Component.onCompleted: {
        _tabsIndicator.initAxisBinding()
    }
}
