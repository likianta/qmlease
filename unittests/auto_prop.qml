import QtQuick
import LKWidgets

Window {
    visible: true
    width: 400
    height: 300

    Rectangle {
        anchors.centerIn: parent
        width: py.myobj.get_width()
        height: 100
        color: '#222435'

        Behavior on width {
            NumberAnimation {
                duration: 300
            }
        }

        Component.onCompleted: {
            console.log('init rect width', this.width)
            py.myobj.width_changed.connect((val) => {
                console.log('width changing', val)
                this.width = val
            })
        }
    }

    ListView {
        anchors {
            horizontalCenter: parent.horizontalCenter
            top: parent.top
            margins: 10
        }
        width: 200
        height: 100
        model: py.myobj.get_model()
        delegate: LKText {
            text: model.name + ' ' + model.age
        }
    }

    LKButton {
        anchors {
            horizontalCenter: parent.horizontalCenter
            bottom: parent.bottom
            margins: 10
        }
        text: 'test'
        onClicked: {
            py.myobj.test_update()
        }
    }
}
