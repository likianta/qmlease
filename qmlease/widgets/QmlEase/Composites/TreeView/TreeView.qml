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

    function extractCheckedTree() {
        const data = []
        let i
        let node
        for (i = 0; i < root.count; i++) {
            node = root.itemAtIndex(i)  // must be a FolderNode
            data.push(..._recurseGettingFolderCheckStates(node))
        }
        return py.qmlease.convert_path_list_to_tree_model(data)
    }

    function _recurseGettingFolderCheckStates(folderNode) {
        let descendantStates
        let subNode
        let partialChecked = false
        let out = []
        if (folderNode.checked) {
            out.push(folderNode.path)
        }
        for (let i = 0; i < folderNode.count; i++) {
            subNode = folderNode.getSubNode(i)
            // if (subNode === null) {
            //     continue
            // }
            if (subNode.checked) {
                out.push(subNode.path)
                partialChecked = true
            }
            if (subNode instanceof FolderNode) {
                const descendantStates = 
                    _recurseGettingFolderCheckStates(subNode)
                if (descendantStates.length > 0) {
                    out.push(...descendantStates)
                    partialChecked = true
                }
            }
        }
        if (partialChecked) {
            out.push(folderNode.path)
        }
        return out
    }

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
