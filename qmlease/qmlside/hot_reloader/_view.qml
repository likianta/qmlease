import QtQuick 2.15
import QtQuick.Window 2.15

// References:
//  https://qml.guide/live-reloading-hot-reloading-qml

Window {
    id: root
    title: "QmlEase Reloader"
    flags: Qt.WindowStaysOnTopHint
    color: '#F2F2F2'
    // visible: true

    property alias source: _loader.source
    signal reloadTriggered()

    Loader {
        id: _loader
        anchors.centerIn: parent
    }

    Rectangle {
        id: _btn
        anchors.centerIn: parent
        width: 160
        height: 60
        color: pycolor.panel_bg

        Text {
            anchors.centerIn: parent
            color: pycolor.text_main
//            color: _area.containsMouse ? '#5F00FF' : '#666666'
            font.pixelSize: 28
            text: 'RELOAD'
        }

        MouseArea {
            id: _area
            anchors.fill: parent
            hoverEnabled: true
            onClicked: root.reloadTriggered()
        }
    }

    function _moveWindowCenter() {
        const scr_width = Screen.width
        const scr_height = Screen.height
        root.x = scr_width / 2 - this.width / 2
        root.y = scr_height / 2 - this.height / 2
        return [root.x, root.y]
    }

    function _moveWindowRightBottom() {
        const scr_width = Screen.width
        const scr_height = Screen.height
        root.x = scr_width - 200 - this.width
        root.y = scr_height - 200 - this.height
        return [root.x, root.y]
    }

    Component.onCompleted: {
        this.width = _btn.width
        this.height = _btn.height
//        const [x, y] = _moveWindowCenter()
        const [x, y] = _moveWindowRightBottom()
        this.visible = true
        // console.log(`HotLoader started! (position at (${x}, ${y}))`)
        py.qmlease.reloader.init_reloader_window(this)
    }
}
