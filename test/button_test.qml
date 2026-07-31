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
        // Button {
        //     Layout.fillWidth: true
        //     border.width: 4
        //     // border.color: pycolor.get(pycolor.theme_blue, 'outline_variant')
        //     // color: pycolor.theme_blue
        //     color: pycolor.get(pycolor.theme_blue, 'rshift')
        //     text: 'Eight Nine Ten'
        // }
        // Button {
        //     text: 'Switch light/dark theme'
        //     onClicked: {
        //         pycolor.dark_theme = !pycolor.dark_theme
        //     }
        // }
    }
}
