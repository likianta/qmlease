/// Container is a stacked layout.

import QtQuick as Q
import QmlEase as E

E.Rectangle {
    border.width: showBorder ? 1 : 0
    radius: 4
    
    default property alias content: contentArea.data
    property bool showBorder: false

    Q.Item {
        id: contentArea
        anchors {
            fill: parent
            margins: parent.border.width
        }
        clip: true
    }
}
