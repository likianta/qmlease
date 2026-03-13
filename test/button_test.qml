import QtQuick
import QtQuick.Layouts
import QmlEase

Window {
    ColumnLayout {
        anchors.centerIn: parent
        width: 240
        spacing: 12
        Button {
            // Layout.fillWidth: true
            text: 'One'
        }
        Button {
            text: 'Two'
        }
        Button {
            text: 'Three Four Five Six Seven'
        }
    }
}
