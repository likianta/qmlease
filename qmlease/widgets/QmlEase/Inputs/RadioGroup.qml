import QtQuick
import QtQuick.Layouts
import QmlEase

ColumnLayout {
    id: root
    spacing: horizontal ? pysize.spacing_s : pysize.spacing_m

    property bool   ghostBorder: false
    property bool   horizontal: false
    property int    index: 0
    property string label
    property var    model  // rename to "options"?

    Item {
//        width: _text.width
//        height: pysize.above_entry_height
        Layout.fillWidth: true
        Layout.preferredHeight: pysize.above_entry_height
        Text {
            id: _text
            anchors.verticalCenter: parent.verticalCenter
            text: root.label
        }
    }

    Loader {
        Layout.fillWidth: !root.horizontal
        Layout.preferredHeight: root.horizontal ? pysize.entry_height : -1
        sourceComponent: root.horizontal ? _rowLayout : _columnLayout
    }

    Component {
        id: _rowLayout
        RowLayout {
//            Layout.fillWidth: true
//            Layout.preferredHeight: pysize.entry_height
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

    Component {
        id: _columnLayout
        ColumnLayout {
            spacing: pysize.spacing_m

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
}
