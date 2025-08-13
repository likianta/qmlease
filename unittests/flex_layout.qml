import QtQuick
import QmlEase

Window {
    GhostBorder {
        anchors.centerIn: parent
        // padding: [24, 12]
        Row {
            Text { text: 'Hello world!' }
            Text { text: 'Long time no see.' }
        }
    }
}
