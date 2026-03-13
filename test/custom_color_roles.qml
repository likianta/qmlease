import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QmlEase

Window {
    width: 600
    height: 400

    component Block: Rectangle {
        width: 240
        height: 40
        property string text
        property string textColor
        Text {
            anchors.centerIn: parent
            text: parent.text
            color: parent.textColor
        }
    }

    ColumnLayout {
        anchors.centerIn: parent
        width: 240
        spacing: 16

        Block {
            color: pycolor.primary
            text: 'Primary'
            textColor: pycolor.on_primary
        }

        Block {
            color: pycolor.theme_blue
            text: 'Theme blue'
            textColor: pycolor.on_theme_blue
        }

        Block {
            color: pycolor.surface_container
            text: 'Green'
            textColor: pycolor.green
        }

        Button {
            text: 'Swith light/dark theme'
            onClicked: {
                pycolor.dark_theme = !pycolor.dark_theme
            }
        }
    }
}
