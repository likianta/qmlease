import QtQuick 2.15
import QtQuick.Window 2.15

import LKWidgets 1.0
import LKWidgets.Controls 1.0

LKWindow {
    id: root
    width: 400
    height: 300

    LKText {
        anchors {
            horizontalCenter: parent.horizontalCenter
            bottom: _text.top
            bottomMargin: 12
        }
        text: 'Press "A" to trigger a key event'
    }

    LKText {
        id: _text
        anchors.centerIn: parent
        font.pixelSize: 24
    }

    LKFocusField {}

    LKFocus {
        Component.onCompleted: {
            this.register(Qt.Key_A, Qt.NoModifier, () => {
                console.log("A")
                _text.text = "A"
            })
        }
    }
}

