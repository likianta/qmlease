import QtQuick
import QtQuick.Layouts
import QmlEase

Window {
    ColumnLayout {
        anchors.centerIn: parent
        spacing: 12

        RowLayout {
            spacing: 12

            TextInput {
                label: 'Text input'
            }

            RadioGroup {
                horizontal: true
                label: 'Radio group'
                model: [
                    'Pamela Fernandez',
                    'Carl Kelly',
                    'Tamara Hall'
                ]
                // Component.onCompleted: {
                //     qmlease.widget.inspect_size(this)
                //     qmlease.widget.inspect_size(this.children[0])
                //     qmlease.widget.inspect_size(this.children[1])
                // }
            }
        }

        RowLayout {
            spacing: 12

            TextInput {
                Layout.alignment: Qt.AlignTop
                label: 'Text input'
            }

            RadioGroup {
                horizontal: false
                label: 'Radio group'
                model: [
                    'Pamela Fernandez',
                    'Carl Kelly',
                    'Tamara Hall'
                ]
            }
        }
    }
}
