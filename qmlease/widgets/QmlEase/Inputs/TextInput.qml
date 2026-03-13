import QtQuick
import QtQuick as Q
import QtQuick.Layouts
import QmlEase

ColumnLayout {
    id: root
    implicitWidth: pysize.bar_width
    spacing: pysize.spacing_s

    property string color: pycolor.surface_container
    property bool   enabled: true
    property string help: ''
    property string label: ''
    property string outlineColor: pycolor.outline_variant
    property string placeholder: ''
    property bool   readonly: false
    property string text: ''
    property bool   _hasContent: text.length > 0

    signal editingFinished()
    
    Item {
        visible: root.label || root.help
        Layout.fillWidth: true
        // height: _label.height
        height: _label.height

        Text {
            id: _label
            visible: root.label != ''
            anchors {
                left: parent.left
                leftMargin: 2
            }
            // font.pixelSize: pyfont.size_s
            text: root.label
        }

        IconButton {
            id: _help
            visible: root.help != ''
            anchors {
                verticalCenter: parent.verticalCenter
                right: parent.right
                rightMargin: 4
            }
        }
    }

    Rectangle {
        Layout.fillWidth: true
        // height: _input.implicitHeight + 12
        height: pysize.bar_height_m
        border.width: _input.activeFocus ? 2 : 0
        border.color: root.outlineColor
        color: root.color
        radius: pysize.radius_l

        Behavior on border.width {
            NumberAnimation {
                duration: 100
            }
        }

        MouseArea {
            anchors.fill: parent
            onClicked: _input.focus = true
        }

        Q.TextInput {
            id: _input
            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                right: parent.right
                margins: 12
            }
            clip: true
            color: pycolor.on_surface
            enabled: root.enabled
            font.family: pyfont.font_default
            font.pixelSize: pyfont.size_m
            readOnly: root.readonly
            selectionColor: pycolor.primary
            text: root.text

            onEditingFinished: root.editingFinished()
            onTextChanged: root.text = text

            Text {
                visible: root.placeholder && !root._hasContent
                anchors.fill: parent
                verticalAlignment: Q.TextInput.AlignVCenter
                font: parent.font
                opacity: 0.5
                text: root.placeholder
            }
        }
    }
}
