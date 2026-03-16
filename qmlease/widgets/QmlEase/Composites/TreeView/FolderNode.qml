import QtQuick
import QtQuick.Layouts
import QmlEase

Item {
    id: root
    width: pysize.entry_width
    height: expanded ?
        _headerRow.height + _entryList.height :
        _headerRow.height

    property bool   checkable
    property bool   checked
    // [{
    //  'type': 'file' | 'folder',
    //  'name': str,
    //  'path': str,
    //  'checked': bool,
    //  'children': [...],  // only for folder
    // }, ...]
    property var    childrenModel: []
    property bool   expanded
    property bool   ghostBorder
    property int    indentation
    property string name
    property string path
    property int    _indicatorSize: 16

    // signal checked()
    signal clicked(string nodeId)

    GuideLine {
        visible: root.indentation > 0
        x: 11
        height: root.height
    }

    ColumnLayout {
        id: _mainBody
        anchors {
            left: parent.left
            right: parent.right
            leftMargin: root.indentation == 0 ? 0 : 24
        }
        // width: parent.width
        spacing: 0

        // header row
        Rectangle {
            id: _headerRow
            Layout.fillWidth: true
            Layout.preferredHeight: pysize.entry_height_s
            border.width: root.ghostBorder && _area.containsMouse ? 1 : 0
            color: pycolor.transparent

            RowLayout {
                anchors {
                    left: parent.left
                    right: parent.right
                    verticalCenter: parent.verticalCenter
                    // margins: 4
                }
                // anchors.fill: parent
                // anchors.verticalCenter: parent.verticalCenter
                // spacing: pysize.spacing

                // arrow expander
                Image {
                    width: root._indicatorSize
                    height: root._indicatorSize
                    fillMode: Image.PreserveAspectFit
                    rotation: root.expanded ? 90 : 0
                    source: './Assets/arrow-right-s-line.svg'
                    Behavior on rotation {
                        NumberAnimation {
                            duration: 100
                        }
                    }
                    // MouseArea {
                    //     anchors.fill: parent
                    //     onClicked: {
                    //         root.expanded = !root.expanded
                    //     }
                    // }
                }

                CheckBoxIndicator {
                    id: _checkbox
                    visible: root.checkable
                    width: root._indicatorSize
                    height: root._indicatorSize
                    checked: root.checked
                }

                Text {
                    Layout.fillWidth: true
//                    Layout.preferredHeight: pysize.entry_height
//                    verticalAlignment: Text.AlignVCenter
                    text: root.name
                }
            }

            MouseArea {
                id: _area
                anchors.fill: parent
                hoverEnabled: true
                onClicked: {
                    root.checked = !root.checked
                    root.expanded = !root.expanded  // test
                    root.clicked(root.path)
                }
            }
        }

        ListView {
            id: _entryList
            Layout.fillWidth: true
            height: root.expanded ? contentHeight : 0
            clip: true
            model: root.childrenModel
            spacing: 0

            // Behavior on height {
            //     NumberAnimation {
            //         duration: 100
            //     }
            // }

            delegate: Loader {
                width: root.width
                source: modelData.type == 'file' ?
                    './FileNode.qml' : './FolderNode.qml'
                onLoaded: {
                    this.item.name = modelData.name
                    this.item.path = modelData.path
                    this.item.checkable = root.checkable
                    this.item.checked = root.checked
                    this.item.ghostBorder = root.ghostBorder
                    this.item.indentation = root.indentation + 1
                    if (modelData.type == 'folder') {
                        this.item.childrenModel = modelData.children
                    }
                    // this.height = Qt.binding(() => this.item.height)
                }
            }
        }
    }
}
