import QtQuick
import LKWidgets

LKWindow {
    id: root

    property alias source: _loader.source
    signal reloadTriggered()

    Loader {
        id: _loader
        anchors.fill: parent
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
    }
}
