import QtQuick
import LKWidgets

LKWindow {
    id: root
    visible: false

    property alias source: _loader.source
    signal reloadTriggered()
    signal reloaded(var item)

    Loader {
        id: _loader
//        onLoaded: root.reloaded(this.item)
        onLoaded: {
            if (this.item.width) {
                root.width = this.item.width
            } else {
                this.item.width = root.width
            }
            if (this.item.height) {
                root.height = this.item.height
            } else {
                this.item.height = root.height
            }
        }
    }

    LKGhostButton {
        anchors {
            top: parent.top
            right: parent.right
            margins: 8
        }
        text: 'Reload'
        onClicked: root.reloadTriggered()
    }

    Component.onCompleted: {
        py.qmlease.reloader.init_reloader_window(this)
        this.visible = true
    }
}
