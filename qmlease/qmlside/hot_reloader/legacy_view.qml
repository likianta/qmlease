import QtQuick 2.15
import QtQuick.Window 2.15

// References:
//  https://qml.guide/live-reloading-hot-reloading-qml

Window {
    visible: true
    color: '#f2f2f2'
    flags: Qt.WindowStaysOnTopHint
    title: "Hot Reloader"

    Loader {
        id: _loader
        anchors.centerIn: parent
        Component.onCompleted: {
            pyloader.set_loader(this)
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
            color: pycolor.text_default
//            color: _area.containsMouse ? '#5f00ff' : '#666666'
            font.pixelSize: 28
            text: 'RELOAD'
        }

        MouseArea {
            id: _area
            anchors.fill: parent
            hoverEnabled: true
            onClicked: pyloader.reload()
        }

//        Component.onCompleted: {
//            this.color = pyloader.get_bg_color()
//        }
    }

    Component.onCompleted: {
        this.width = _btn.width
        this.height = _btn.height
        // move window to right-center.
        const scr_width = Screen.width
        const scr_height = Screen.height
        this.x = scr_width - 200 - this.width
        this.y = scr_height / 2 - this.height / 2
        this.visible = true
        console.log(`HotLoader started! (position at [${this.x}, ${this.y}])`)
    }
}
