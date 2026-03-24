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
            text: 'One'
        }
        Button {
            Layout.fillWidth: true
            text: 'Two'
        }
        Button {
            text: 'Three Four Five Six Seven'
        }
        Button {
            border.width: 2
            border.color: pycolor.get(pycolor.theme_blue, 'outline_variant')
            // color: pycolor.theme_blue
            color: pycolor.get(pycolor.theme_blue, 'darker')
            text: 'Eight Nine Ten'
            textColor: pycolor.on_theme_blue
        }
        // Button {
        //     border.width: 2
        //     border.color: pycolor.theme_blue_outline_variant
        //     // border.color: pycolor.red
        //     color: pycolor.theme_blue_container
        //     text: 'Eleven Twelve Thirteen'
        //     textColor: pycolor.on_theme_blue
        // }
        Button {
            text: 'Switch light/dark theme'
            onClicked: {
                pycolor.dark_theme = !pycolor.dark_theme
            }
        }
    }
}
