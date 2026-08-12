import QtQuick
import QmlEase

Window {
    id: root
    property int counter: 0

    Row {
        anchors.centerIn: parent
        spacing: 12
        border: true

        Text {
            text: `Counter: ${root.counter}`
        }

        Button {
            text: "Increment"
            onClicked: {
                root.counter += 1
            }
        }
    }
}