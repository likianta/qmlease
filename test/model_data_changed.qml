import QtQuick
import QtQuick.Layouts
import QmlEase

Window {
    ColumnLayout {
        anchors {
            fill: parent
            margins: 12
        }
        ListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            delegate: Text {
                text: (
                    `index: ${model.index}; ` +
                    `name: ${model.name}; ` +
                    `age: ${model.age}`
                )
            }
            Component.onCompleted: {
                py.main.init_model(this)
            }
        }
        Button {
            text: 'Random item'
            onClicked: {
                py.main.change_some_item_name()
            }
        }
    }
}
