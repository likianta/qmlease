import QtQuick
import LKWidgets
import LKWidgets.Progress

LKWindow {

    LKCircleProgress {
        id: _prog
        anchors.centerIn: parent
    }

    Timer {
        id: _timer
        running: false
        repeat: true
        interval: 100
        onTriggered:{
            _prog.value += 0.1
            if (_prog.value >= 1) {
                this.running = false
            }
//            _prog.canvas.requestPaint()
        }
    }

    LKButton {
        anchors {
            horizontalCenter: parent.horizontalCenter
            bottom: parent.bottom
            margins: 8
        }
        text: "Start"
        onClicked: {
            _timer.running = !_timer.running
            text = _timer.running ? "Stop" : "Start"
        }
    }
}
