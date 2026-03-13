import QtQuick
import QtQuick.Layouts
import QmlEase

ColumnLayout {
    id: root
    spacing: pysize.spacing_s

    property bool   ghostBorder: false
    property int    index: 0
    property string label
    property var    model  // rename to "options"?

    Text {
        text: root.label
    }

    RowLayout {  // options
        Layout.fillWidth: true
        height: pysize.bar_height
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
