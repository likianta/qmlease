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

    Text {
        id: _text
        Layout.preferredHeight: pysize.above_entry_height
        text: root.label
        verticalAlignment: Text.AlignVCenter
    }

    Loader {
        sourceComponent: root.horizontal ? _rowLayout : _columnLayout
    }

    Component {
        id: _rowLayout
        RowLayout {
            // Layout.fillWidth: true
            Layout.preferredHeight: pysize.entry_height
            spacing: pysize.spacing_m

            Repeater {
                model: root.model
                delegate: RadioBox {
                    Layout.fillHeight: true
                    checked: model.index == root.index
                    ghostBorder: root.ghostBorder
                    text: modelData
                    onClicked: root.index = model.index
                }
            }
        }
    }

    Component {
        id: _columnLayout
        ColumnLayout {
            spacing: pysize.spacing_s
            Repeater {
                model: root.model
                delegate: RadioBox {
                    Layout.fillWidth: true
                    Layout.preferredHeight: pysize.entry_height_s
                    checked: model.index == root.index
                    ghostBorder: root.ghostBorder
                    text: modelData
                    onClicked: root.index = model.index
                }
            }
            // Component.onCompleted: {
            //     py.qmlease.inspect_size(this)
            // }
        }
    }
}
