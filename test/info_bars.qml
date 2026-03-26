import QtQuick
import QtQuick.Layouts
import QmlEase
import QmlEase.Visual

Window {
    Vertical {
        id: _layout
        anchors {
            centerIn: parent
        }
        width: parent.width - 80

        property bool bold: false

        Info {
            Layout.fillWidth: true
            bold: _layout.bold
            text: 'Smile half end across before. Effort space ready wait program. Sign seem city exist light ever business.'
            type: 'info'
        }

        Info {
            Layout.fillWidth: true
            bold: _layout.bold
            text: 'Candidate probably while college. Treatment with chance service bag.'
            type: 'success'
        }

        Info {
            Layout.fillWidth: true
            bold: _layout.bold
            text: 'Side foreign enough school. Attention course future easy long situation choice.'
            type: 'warning'
        }
        
        Info {
            Layout.fillWidth: true
            bold: _layout.bold
            text: 'Seven campaign remember year. West seven article drug since kid. Mother spring discuss indicate.'
            type: 'error'
        }

        Horizontal {
            Button {
                text: 'Switch "bold"'
                onClicked: {
                    _layout.bold = !_layout.bold
                }
            }
            Button {
                text: 'Switch theme'
                onClicked: {
                    pycolor.dark_theme = !pycolor.dark_theme
                }
            }
        }
    }
}
