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
    property var    childrenModel
    property alias  count: _entryList.count
    property bool   expanded
    property bool   ghostBorder
    property int    indentation
    property string name
    property string path
    property int    _indicatorSize: 16
    // property QtObject _pyctrl: py.qmlease.init_control(root, 'TreeView')
    // readonly property int count: _entryList.count

    signal nodeChecked(string path, bool checked)
    signal nodeClicked(string path)

    function applyCheckStates(value) {
        root.checked = value
        for (let i = 0; i < _entryList.count; i++) {
            _entryList.itemAtIndex(i).item.applyCheckStates(value)
        }
    }

    function getSubNode(index) {
        return _entryList.itemAtIndex(index).item
    }

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
                    id: _arrow
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
                    //     id: _arrowArea
                    //     anchors.fill: parent
                    //     hoverEnabled: true
                    //     preventStealing: true
                    //     onEntered: {
                    //         console.log('arrow area entered')
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
                    id: _headerText
                    Layout.fillWidth: true
                    text: root.name
                }
            }

            MouseArea {
                id: _area
                anchors.fill: parent
                hoverEnabled: true
                // propagateComposedEvents: true
                onClicked: (e) => {
                    if (e.x < _arrow.width) {
                        root.expanded = !root.expanded
                    } else {
                        root.applyCheckStates(!root.checked)
                        if (root.checkable) {
                            root.nodeChecked(root.path, root.checked)
                        }
                        root.nodeClicked(root.path)
                    }
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
                width: _entryList.width
                source: model.type == 'file' ?
                    './FileNode.qml' : './FolderNode.qml'
                onLoaded: {
                    this.item.name = model.name
                    this.item.path = model.path
                    this.item.checkable = root.checkable
                    this.item.checked = root.checked
                    this.item.ghostBorder = root.ghostBorder
                    this.item.indentation = root.indentation + 1
                    this.item.nodeChecked.connect(root.nodeChecked)
                    if (model.type == 'folder') {
                        this.item.childrenModel = model.children
                    }
                }
            }
        }
    }
}
