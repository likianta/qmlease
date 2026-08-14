import QmlEase
import QmlEase.Visual

Window {
    Row {
        anchors.centerIn: parent
        // width: 200
        // height: 80
        valign: 'center'
        
        StatusIndicator {
            id: indicator
            width: 200
        }
        
        Button {
            text: 'Change status'
            onClicked: {
                switch (indicator.status) {
                    case 'idle':
                        indicator.status = 'info'
                        break
                    case 'info':
                        indicator.status = 'success'
                        break
                    case 'success':
                        indicator.status = 'warning'
                        break
                    case 'warning':
                        indicator.status = 'error'
                        break
                    case 'error':
                        indicator.status = 'idle'
                        break
                }
            }
        }
    }
}