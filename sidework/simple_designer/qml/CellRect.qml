import QtQuick
import QtQuick.Layouts
import LKWidgets

Item {
    id: root
    width: 300
    height: 20

    property string color
    property int    index
    property string label
    property bool   selected: false

    signal forceFocused(int index)

    function activate() {
        _color_input.activate()
    }

    RowLayout {
        anchors.fill: parent

        LKRectangle {
            id: _cell
            Layout.preferredWidth: 100
            Layout.fillHeight: true
            border.width: root.selected ? 1 : 0
            border.color: '#b2b2b2'

            Behavior on color {
                ColorAnimation {
                    duration: 200
                }
            }
        }

        LKInput {
            id: _color_input
            Layout.fillWidth: true
            Layout.fillHeight: true
            inputMask: '>HHHHHH;0'
            onClicked: {
                root.forceFocused(root.index)
            }
            onDisplayTextChanged: {
                _cell.color = '#' + this.displayText
            }
        }

        LKInput {
            id: _token
            Layout.preferredWidth: 120
            Layout.fillHeight: true
            onClicked: {
                root.forceFocused(root.index)
            }
        }
    }

    Component.onCompleted: {
        _color_input.text = root.color
        _token.text = root.label
    }
}
