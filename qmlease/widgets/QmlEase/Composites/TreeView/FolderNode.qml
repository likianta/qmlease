import QtQuick
import QtQuick.Layouts
import QmlEase

Item {
    id: root
    width: pysize.entry_width
    height: _mainBody.height

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
    property bool   expanded
    property bool   ghostBorder
    property string name
    property string path

    // signal checked()
    signal clicked(string nodeId)

    ColumnLayout {
        id: _mainBody
        width: parent.width

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: pysize.entry_height
            border.width: root.ghostBorder && _area.containsMouse ? 1 : 0
            color: pycolor.transparent

            RowLayout {
                // anchors.fill: parent
                anchors.verticalCenter: parent.verticalCenter
                spacing: pysize.spacing

                // TODO
                Rectangle {
                    border.width: 1
                    Text {
                        text: root.expanded ? 'V' : '>'
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            root.expanded = !root.expanded
                        }
                    }
                }

                CheckBoxIndicator {
                    id: _checkbox
                    visible: root.checkable
                    checked: root.checked
                }

                Text {
//                    Layout.fillWidth: true
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
                    root.clicked(root.path)
                }
            }
        }

        ListView {
            Layout.fillWidth: true
            model: root.childrenModel
            delegate: Loader {
                width: root.width
                source: model.type == 'file' ?
                    './FileNode.qml' : './FolderNode.qml'
                onLoaded: {
                    this.item.name = Qt.binding(() => modelData.name)
                    this.item.path = Qt.binding(() => modelData.path)
                    this.item.checkable = root.checkable
                    this.item.checked = root.checked
                    this.item.ghostBorder = root.ghostBorder
                    if (modelData.type == 'folder') {
                        this.item.childrenModel = modelData.children_
                    }
                    console.log(
                        model.index,
                        modelData.type,
                        modelData.name,
                        modelData.path,
                    )
                }
            }
        }
    }

    Component.onCompleted: {
        console.log(
            // model.index,
            // model.type,
            this.name,
            this.path,
            this.checked,
            this.childrenModel.length,
        )
    }
}
