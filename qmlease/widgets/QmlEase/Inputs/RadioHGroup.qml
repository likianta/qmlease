import QtQuick
import QtQuick.Layouts
import QmlEase

ColumnLayout {
    id: root
    spacing: pysize.spacing_s

    property bool   ghostBorder: false
    property bool   horizontal: false
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

    RowLayout {
        Layout.fillWidth: true
        Layout.preferredHeight: pysize.entry_height
        // height: pysize.entry_height
        spacing: pysize.spacing_l

        Repeater {
            model: root.model
            delegate: RadioBox {
                checked: model.index == root.index
                onClicked: root.index = model.index
            }
        }
    }
}
