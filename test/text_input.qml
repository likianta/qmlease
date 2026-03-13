import QtQuick
import QtQuick.Layouts
import QmlEase

Window {
    width: 600
    height: 400

    ColumnLayout {
        anchors.centerIn: parent
        width: 240
        spacing: pysize.spacing

        TextInput {
            id: _input
            Layout.fillWidth: true
            // color: pycolor.surface_container_low
            label: 'AAA'
            placeholder: 'BBB'
            text: 'CCC'
        }

        TextInput {
            Layout.fillWidth: true
            // color: pycolor.surface_container
            label: 'DDD'
            placeholder: 'EEE'
            text: ''
        }

        TextInput {
            Layout.fillWidth: true
            // color: pycolor.surface_variant
            label: 'FFF'
            placeholder: 'GGG'
            text: ''
        }
    }
}
