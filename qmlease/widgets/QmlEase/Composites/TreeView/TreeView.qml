import QtQuick
import QmlEase

ListView {
    id: root
    width: pysize.entry_width

    property bool checkable: false
    property bool expandRoot: false  // affect only top nodes
    property bool ghostBorder: true

    signal nodeChecked(string path, bool checked)
    signal nodeClicked(string path)

    delegate: FolderNode {
        width: root.width
        checkable: root.checkable
        childrenModel: model.children
        expanded: root.expandRoot
        ghostBorder: root.ghostBorder
        name: model.name
        path: model.path
        Component.onCompleted: {
            this.nodeChecked.connect(root.nodeChecked)
        }
    }
}
