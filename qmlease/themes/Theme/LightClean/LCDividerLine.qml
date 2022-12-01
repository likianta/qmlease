import QtQuick 2.15
import "./LCStyle/palette.js" as LCPalette

Rectangle {
    id: _root
    color: LCPalette.BorderNormal
    width: 1; height: 1

    property alias p_color: _root.color
    property string p_orientation: 'horizontal'

    Component.onCompleted: {
        switch (p_orientation) {
            case "h":
                // fall down
            case "horizontal":
                _root.width = parent.width
                break
            case "v":
                // fall down
            case "vertical":
                _root.height = parent.height
                break
        }
    }
}
