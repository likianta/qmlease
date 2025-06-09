import QtQuick
import LKWidgets

Item {
    width: 320
    height: 520
    LKColumn {
        anchors.centerIn: parent
        LKButton {
            text: 'Click me 123'
        }
        LKButton {
            text: 'Click me 456'
        }
    }
}
