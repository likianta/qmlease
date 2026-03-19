import QtQuick
import QmlEase

Rectangle {
    border.width: 0
    border.color: pycolor.outline_variant
    color: pycolor.transparent
    
    default property alias content: _content.data
    property int padding

    Item {
        id: _content
        anchors {
            fill: parent
            margins: 
                parent.padding ? 
                parent.padding : 
                (parent.border.width ? pysize.padding_s : 0)
        }
        clip: true
    }
}
