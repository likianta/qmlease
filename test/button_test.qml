import QtQuick
import QtQuick.Layouts
import QmlEase

Window {
    Vertical {
        anchors.centerIn: parent
        width: 240
        // placeItemsStart: true
        spacing: 12
        Button {
            Layout.fillWidth: true
            text: 'One Two Three'
        }
        Button {
            text: 'Four Five Six Seven'
        }
        Button {
            Layout.fillWidth: true
            border.width: 4
            border.color: pycolor.lower(color, 2)
            color: pycolor.solid_brand
            text: 'Eight Nine Ten'
            textColor: pycolor.on_solid_brand
        }
        Button {
            text: 'Switch light/dark theme'
            onClicked: {
                pycolor.dark_theme = !pycolor.dark_theme
            }
        }
    }
}
