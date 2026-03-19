// FIXME: Repeater doesn't work, this code pattern and its idea may be 
// impossible in QML's mechanism. Use `./Container2.qml` instead.

// https://chatgpt.com/share/69bba2b1-6a7c-800a-a5c9-dcaee8a08190
import QtQuick
import QtQuick.Layouts
import QmlEase

Item {
    id: root
    // implicitWidth: _layout.implicitWidth
    // implicitHeight: _layout.implicitHeight

    default property alias content: _content.data
    // default property alias content: _loader.item.data
    // readonly property Item _layout: _loader.item
    property bool   border: false
    property string borderColor: pycolor.outline_variant
    property string color: pycolor.transparent
    property bool   horizontal: false
    property int    padding: pysize.padding_s
    property int    spacing: pysize.spacing

    Item {
        id: _content
        visible: false
    }

    Rectangle {
        anchors.fill: parent
        border.width: root.border ? 1 : 0
        border.color: root.borderColor
        color: root.color
    }

    Loader {
        id: _loader
        anchors.fill: parent
        anchors.margins: root.padding
        sourceComponent: root.horizontal ? _row : _column
    }

    Component {
        id: _row
        RowLayout {
            spacing: root.spacing
            Repeater {
                model: _content.data
                delegate: modelData
            }
        }
    }

    Component {
        id: _column
        ColumnLayout {
            spacing: root.spacing
            Repeater {
                model: _content.data
                delegate: modelData
            }
            // data: _content.data
            // default property alias content: _content.data
        }
    }
}
