import QtQuick

ListView {
    property Item   fileItem
    property Item   folderItem
    property string root

    onRootChanged: {
        if (this.root) {
            py.qmlease.widget.load_tree(this, this.root)
        }
    }
}
