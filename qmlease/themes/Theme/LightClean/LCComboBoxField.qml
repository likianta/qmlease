import QtQuick
import QtQuick.Controls
import "LCButtons" as LCB

LCRectangle {
    id: root
    width: 220
    height: 32
    color: '#eeeeee'

    property alias p_title: txt.text
    property int   p_index: 0
    property alias p_model: combox.p_model

    LCText {
        id: txt
        anchors.left: parent.left
        anchors.leftMargin: 12
        anchors.verticalCenter: parent.verticalCenter
    }

    LCB.LCComboBox {
        id: combox
        anchors.right: parent.right
        anchors.rightMargin: 6
        anchors.verticalCenter: parent.verticalCenter
        width: 72
        height: 24

        Component.onCompleted: {
            //  pass
        }
    }
}
