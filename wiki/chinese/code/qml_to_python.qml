import QtQuick

Window {
    visible: true
    width: 400
    height: 300

    Text {
        width: 200
        x: 50
        y: 80
        Component.onCompleted: {
            py.main.set_text_view(this)
        }
    }

    Text {
        width: 80
        x: 50
        y: 180
        Component.onCompleted: {
            py.main.set_text_view(this)
        }
    }
}