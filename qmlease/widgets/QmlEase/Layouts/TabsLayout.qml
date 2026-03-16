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
                        onClicked: {
                            if (root.index != model.index) {
                                _indicatorLine.moveForward = (
                                    model.index > root.index ? true : false
                                )
                                const titleTab = _titleTabs.itemAt(model.index)
                                _stickyStartPoint.x = titleTab.x
                                _stickyEndPoint.x = titleTab.x + titleTab.width
                                root.index = model.index
                            }
                        }
                    }
                }
            }
        }

        // full-width divider line (grey)
        Rectangle {
            id: _indicatorLine
            Layout.fillWidth: true
            Layout.preferredHeight: 2
            clip: false
            color: pycolor.surface_container_high

//            Rectangle {
//                id: _indicatorLineAbove
//                // x: _titleTabs.itemAt(root.index).x
//                // width: _titleTabs.itemAt(root.index).width
//                width: 0
//                height: parent.height + 2
//                color: pycolor.theme_blue
//
//                property int fromWidth
//                property int toWidth
//
//                function initAxisBinding() {
//                    this.x = Qt.binding(
//                        () => _titleTabs.itemAt(root.index).x
//                    )
//                    this.width = Qt.binding(
//                        () => _titleTabs.itemAt(root.index).width
//                    )
//                }
//
//                Behavior on x {
//                    NumberAnimation {
//                        duration: 150
//                        easing.type: Easing.OutCubic
//                    }
//                }
//
//                SequentialAnimation {
//                    id: _indicatorWidthAnim
//                    NumberAnimation {
//                        target: _indicatorLineAbove
//                        duration: 90
//                        easing.type: Easing.InCubic
//                        property: 'width'
//                        to: (
//                            _indicatorLineAbove.fromWidth +
//                            _indicatorLineAbove.toWidth
//                        ) * 0.7
//                    }
//                    NumberAnimation {
//                        target: _indicatorLineAbove
//                        duration: 60
//                        easing.type: Easing.OutCubic
//                        property: 'width'
//                        to: _indicatorLineAbove.toWidth
//                    }
//                }
//            }

            property bool moveForward: true
//            property int  _fastMotion: Easing.OutCubic
//            property int  _longTime: 150
//            property int  _shortTime: 100
//            property int  _slowMotion: Easing.InCubic

            // sticky indicator animation
            Item {
                id: _stickyStartPoint
                x: 0
                Behavior on x {
                    NumberAnimation {
                        id: _animStartPoint
                        duration: _indicatorLine.moveForward ? 200 : 150
                        easing.type: _indicatorLine.moveForward ?
                            Easing.InCubic : Easing.OutCubic
                    }
                }
            }

            Item {
                id: _stickyEndPoint
                x: 0
                Behavior on x {
                    NumberAnimation {
                        id: _animEndPoint
                        duration: _indicatorLine.moveForward ? 150 : 200
                        easing.type: _indicatorLine.moveForward ?
                            Easing.OutCubic : Easing.InCubic
                    }
                }
            }

            Rectangle {
                x: _stickyStartPoint.x
                width: _stickyEndPoint.x - _stickyStartPoint.x
                height: parent.height
                color: pycolor.theme_blue
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
        // _indicatorLineAbove.initAxisBinding()
        const titleTab = _titleTabs.itemAt(root.index)
        _stickyStartPoint.x = titleTab.x
        _stickyEndPoint.x = titleTab.x + titleTab.width
    }
}
