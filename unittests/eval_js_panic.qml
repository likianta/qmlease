import QtQuick

Window {
    id: root
    objectName: 'root'
    visible: true
    Component.onCompleted: {
        py.main.test(root)
    }
}
