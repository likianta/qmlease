import QtQuick
import QtQuick.Layouts
import QmlEase

ListView {
    id: root
    width: pysize.entry_width

    property bool checkable: false
    property bool ghostBorder: true
    property bool multipleSelectable: false

    signal nodeClicked(string nodeId)

    delegate: FolderNode {
        width: root.width
        checkable: root.checkable
        checked: modelData.checked
        childrenModel: modelData.children
        ghostBorder: root.ghostBorder
        name: modelData.name
        path: modelData.path
    }
}
