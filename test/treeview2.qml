import QtQuick
import QtQuick.Layouts
import QmlEase
import QmlEase.Composites

Window {
    id: root

    property var model
    signal pathSubmit(string path)

    ColumnLayout {
        anchors {
            fill: parent
            margins: 24
        }
        TextInput {
            Layout.fillWidth: true
            label: 'Input directory'
            onEditingFinished: (path) => root.pathSubmit(path)
        }
        TreeView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            checkable: true
            expandRoot: true
            model: root.model
        }
    }

    Component.onCompleted: {
        py.main.init_ui(this)
    }
}
