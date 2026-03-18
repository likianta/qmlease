import QtQuick
import QtQuick.Window

Window {
    visible: true
    width: 800
    height: 600

    ListView {
        anchors {
            fill: parent
            margins: 24
        }
        model: ListModel {
            ListElement {
                name: 'AAA'
                number: 111
            }
            ListElement {
                name: 'BBB'
                number: 222
            }
        }
        delegate: Text { 
            text: `Name: ${model.name}; Number: ${model.number}` 
        }
        Component.onCompleted: {
            main.test(this)
        }
    }
}
