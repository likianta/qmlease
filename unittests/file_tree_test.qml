import QtQuick
import QmlEase
import QmlEase.Integrated

Window {
    Item {
        anchors.centerIn: parent
        FolderNode {
            checkable: true
            text: 'Some folder'
        }
        Component.onCompleted: {
            py.qmlease.inspect_size(this)
        }
    }
}
