import QtQuick 2.15
import ".." as A

Item {
    id: root
    width: _row.implicitWidth
    height: _row.implicitHeight

    // default property alias data: _row.data

    property alias alignment: _row.alignment
    property alias autoSize: _row.autoSize
    property alias border: _rect.border
    property alias color: _rect.color
    property int   debug: 0
    property alias delegateChildren: _row.data

    A.LKRectangle2 {
        id: _rect
        visible: root.debug > 0
        anchors.fill: parent
        border.width: root.debug > 0 ? 1 : 0
        border.color: {
            if (root.debug == 2) {
                return borderColor1
            } else if (root.debug == 1) {
                if (mouseEntered) {
                    return borderColor1
                } else {
                    return borderColor0
                }
            } else {
                return borderColor0
            }
        }
        color: 'transparent'
    }

    LKColumn {
        id: _row
        anchors.fill: parent
    }
}
