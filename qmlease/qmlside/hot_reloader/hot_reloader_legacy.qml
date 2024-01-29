import QtQuick 2.15
import QtQuick.Window 2.15

// References:
//  https://qml.guide/live-reloading-hot-reloading-qml

Window {
    id: root
    title: "Hot Reloader"
    flags: Qt.WindowStaysOnTopHint
    color: '#F2F2F2'
    // visible: true

    Loader {
        id: _loader
        anchors.centerIn: parent
        Component.onCompleted: {
            py.qmloader.set_loader(this)
        }
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
            onClicked: py.qmloader.reload()
        }

//        Component.onCompleted: {
//            this.color = py.qmloader.get_bg_color()
//        }
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
        console.log(`HotLoader started! (position at (${x}, ${y}))`)
    }
}
