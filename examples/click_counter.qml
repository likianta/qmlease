import QmlEase

Window {
    id: root
    property int counter: 0

    Row {
        anchors.centerIn: parent
        valign: 'center'
        lpadding: 24
        rpadding: 8
        vpadding: 8
        spacing: 40
        border: true
        borderColor: pycolor.outline_thin
        color: pycolor.panel

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