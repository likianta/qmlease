import QtQuick

Window {
    visible: true

    Rectangle {
        id: rect0
        anchors.centerIn: parent
        width: 100
        height: 100
        color: 'red'

        Rectangle {
            id: rect1
            width: 30
            height: 30
            color: 'green'
        }
    }

    Component.onCompleted: {
        py.main.test(rect0, rect1)
    }
}
