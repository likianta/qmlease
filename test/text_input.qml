import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QmlEase

Window {
    width: 600
    height: 400

    ColumnLayout {
        anchors.centerIn: parent
        width: 240
        spacing: 16

        TextInput {
            id: _input
            Layout.fillWidth: true
            label: 'Theme blue outline'
            // outlineColor: '#0969DA'
            outlineColor: pycolor.theme_blue
            placeholder: 'BBB'
            text: 'CCC'
        }

        TextInput {
            Layout.fillWidth: true
            label: 'Primary outline'
            outlineColor: pycolor.primary
            placeholder: 'EEE'
            text: ''
        }

        TextInput {
            Layout.fillWidth: true
            // color: pycolor.surface_variant
            label: 'Default outline'
            placeholder: 'GGG'
            text: ''
        }

        TextInput {
            Layout.fillWidth: true
            label: 'Success outline'
            outlineColor: pycolor.success
            placeholder: 'GGG'
            text: ''
        }

        Button {
            text: 'Swith light/dark theme'
            onClicked: {
                pycolor.dark_theme = !pycolor.dark_theme
            }
        }
    }
}
