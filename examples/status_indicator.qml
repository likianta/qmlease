import QtQuick
import QmlEase
import QmlEase.Visual

Window {
    Row {
        anchors.centerIn: parent
        valign: 'center'
        hpadding: 16
        vpadding: 8
        spacing: 16
        color: pycolor.panel

        StatusIndicator {
            id: stat
            maxTextWidth: measureTextWidth('DISCONNECTED')
            text: status == 'idle' ? 
                'IDLE' : status == 'success' ? 'CONNECTED' : 'DISCONNECTED'
            Component.onCompleted: {
                console.log('maxTextWidth:', maxTextWidth)
            }
        }

        Button {
            text: 'Change status'
            onClicked: {
                stat.status = (
                    stat.status === 'idle' ? 'success' :
                    stat.status === 'success' ? 'error' :
                    stat.status === 'error' ? 'idle' :
                    ''
                )
            }
        }
    }
}