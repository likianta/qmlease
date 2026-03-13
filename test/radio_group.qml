import QtQuick
import QtQuick.Layouts
import QmlEase

Window {
    ColumnLayout {
        anchors.centerIn: parent
        width: 240
        spacing: 12

        RadioGroup {
            label: 'Select one option from radio group'
            model: ['One', 'Two', 'Three Four Five Six Seven']
        }
    }
}
