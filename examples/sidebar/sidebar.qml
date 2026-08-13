import QtQuick
import QmlEase
import QmlEase.Layouts

Window {
    width: 900
    height: 720

    Sidebar {
        anchors {
            left: parent.left
            top: parent.top
            bottom: parent.bottom
            margins: 8
        }
        width: 240
        model: py.sidebar.init_model()
    }
}