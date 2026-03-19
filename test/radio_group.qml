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
                ghostBorder: true
                horizontal: true
                label: 'Radio group'
                model: [
                    'Pamela Fernandez',
                    'Carl Kelly',
                    'Tamara Hall'
                ]
                // Component.onCompleted: {
                //     py.qmlease.inspect_size(this)
                //     py.qmlease.inspect_size(this.children[0])
                //     py.qmlease.inspect_size(this.children[1])
                // }
            }
        }

        RowLayout {
            spacing: 12

            TextInput {
                Layout.alignment: Qt.AlignTop
                Layout.fillWidth: true
                label: 'Text input'
            }

            RadioGroup {
                id: vradio
                // Layout.preferredWidth: py.qmlease.get_longest_text_width(model)
                ghostBorder: true
                horizontal: false
                label: 'Radio group'
                model: [
                    'Jeffery Hill',
                    'Eric Chambers',
                    'Kevin Gregory'
                ]
            }
            
            Component.onCompleted: {
                py.qmlease.inspect_size(vradio, 'vertical radio group')
                console.log(py.qmlease.get_longest_text_width(vradio.model))
            }
        }
    }
}
