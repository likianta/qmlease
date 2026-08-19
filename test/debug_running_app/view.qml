import QtQuick
import QmlEase

Window {
    visible: false // for AI debug, there is no need to show the window
    Button {
        objectName: 'testButton'
        text: 'Test Button'
        onClicked: {
            console.log('test button is clicked')
        }
    }
    Component.onCompleted: {
        py.main.test_ui(this)
    }
}