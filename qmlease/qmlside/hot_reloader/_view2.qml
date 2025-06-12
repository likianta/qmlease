import QtQuick
import LKWidgets

LKWindow {
    id: root
    visible: false
//    width: _loader.width
//    height: _loader.height

    property alias source: _loader.source
    signal loaded(var item)
    signal reloadTriggered()

    Loader {
        id: _loader
        onLoaded: root.loaded(this.item)
//        onLoaded: {
//            if (this.item.width && this.item.height) {
//                this.width = this.item.width
//                this.height = this.item.height
//            } else {
//                this.width = 800
//                this.height = 600
//            }
//        }
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
