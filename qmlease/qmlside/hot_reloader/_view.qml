import QtQuick 2.15
import QtQuick.Window 2.15

// References:
//  https://qml.guide/live-reloading-hot-reloading-qml

Window {
    id: root
    title: "QmlEase Reloader"
    width: 200
    height: 120
    color: '#F2F2F2'
    flags: Qt.WindowStaysOnTopHint
    // visible: true

    property alias source: _loader.source
    signal reloadTriggered()

    Loader {
        id: _loader
        anchors.centerIn: parent
        onLoaded: {
            _moveWindowCenter(this.item)
        }
    }

    Rectangle {
        id: _btn
        anchors.fill: parent
//        anchors.centerIn: parent
//        width: 160
//        height: 60
        color: pycolor.panel_bg

        Text {
            anchors.centerIn: parent
            color: pycolor.text_default
//            color: _area.containsMouse ? '#5F00FF' : '#666666'
            font.pixelSize: 28
            text: 'RELOAD'
        }
    }

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: true
        onClicked: root.reloadTriggered()
    }

    function _moveWindowCenter(win) {
        const scr_width = Screen.width
        const scr_height = Screen.height
        win.x = scr_width / 2 - win.width / 2
        win.y = scr_height / 2 - win.height / 2
        return [win.x, win.y]
    }

    function _moveWindowRightBottom(win) {
        const scr_width = Screen.width
        const scr_height = Screen.height
        win.x = scr_width - 20 - win.width
        win.y = scr_height - 80 - win.height
        return [win.x, win.y]
    }

    Component.onCompleted: {
//        this.width = _btn.width
//        this.height = _btn.height
//        const [x, y] = _moveWindowCenter(this)
        _moveWindowRightBottom(this)
        // const [x, y] = _moveWindowRightBottom()
        // console.log(`HotLoader started! (position at (${x}, ${y}))`)
        py.qmlease.reloader.init_reloader_window(this)
        this.visible = true
    }
}
