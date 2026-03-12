import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QmlEase

Window {
    width: 640
    height: 480

    ColumnLayout {
        Button {
            text: 'Switch to dark'
            onClicked: {
                pycolor.dark_theme = true
            }
        }
        
        Button {
            text: 'Switch to light'
            onClicked: {
                pycolor.dark_theme = false
            }
        }
    }
}
