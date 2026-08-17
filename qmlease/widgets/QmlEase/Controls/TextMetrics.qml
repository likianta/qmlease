import QtQuick

TextMetrics {
    id: root
    font.pixelSize: 12

    readonly property int currentWidth: width
    property var target

    onTargetChanged: {
        if (target && target.font) {
            root.font = target.font
        }
    }

    function getTextLength(text) {
        root.text = text
        return root.width
    }
}