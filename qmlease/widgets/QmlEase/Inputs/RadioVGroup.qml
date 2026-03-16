import QtQuick
import QtQuick.Layouts
import QmlEase

ColumnLayout {
    id: root
    spacing: pysize.spacing

    property bool   ghostBorder: false
    property int    index: 0
    property string label
    property var    model  // rename to "options"?

    Item {
        width: _text.width
        height: pysize.above_entry_height
        Text {
            id: _text
            anchors.verticalCenter: parent.verticalCenter
            text: root.label
        }
    }

    ColumnLayout {
        // Layout.fillWidth: true
        // height: pysize.entry_height
        spacing: pysize.spacing

        Repeater {
            model: root.model
            delegate: RadioBox {
                // height: pysize.entry_height
                checked: model.index == root.index
                onClicked: root.index = model.index
            }
        }
    }
}
