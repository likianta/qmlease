import QtQuick
import QtQuick.Layouts
import QmlEase
import QmlEase.Visual

Window {
    Vertical {
        anchors {
            centerIn: parent
        }
        width: parent.width - 80

        Info {
            Layout.fillWidth: true
            text: 'Smile half end across before. Effort space ready wait program. Sign seem city exist light ever business.'
            type: 'info'
        }

        Info {
            Layout.fillWidth: true
            text: 'Candidate probably while college. Treatment with chance service bag.'
            type: 'success'
        }

        Info {
            Layout.fillWidth: true
            text: 'Side foreign enough school. Attention course future easy long situation choice.'
            type: 'warning'
        }
        
        Info {
            Layout.fillWidth: true
            text: 'Seven campaign remember year. West seven article drug since kid. Mother spring discuss indicate.'
            type: 'error'
        }
    }
}