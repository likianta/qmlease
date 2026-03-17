import QtQuick
import QtQuick as Q
import QtQuick.Layouts
import QmlEase

ColumnLayout {
    id: root
    // implicitWidth: pysize.long_entry_width
    width: pysize.long_entry_width
    // spacing: pysize.spacing_s

    property string color: pycolor.surface_container
    property bool   enabled: true
    property string help
    property string label
    property string outlineColor: pycolor.outline_variant
    property string placeholder
    property bool   readonly: false
    property bool   showEditingHint: false
    property string text
    property bool   _hasContent: text.length > 0
    property bool   _userEdited: false

    signal editingFinished(string text)
    
    Item {
        visible: root.label || root.help
        Layout.fillWidth: true
        // height: _label.height
        height: pysize.above_entry_height
        clip: true

        Text {
            id: _label
            visible: root.label != ''
            anchors {
                left: parent.left
                leftMargin: 2
                verticalCenter: parent.verticalCenter
            }
            color: root.enabled ? pycolor.on_surface : pycolor.outline
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
        id: _inputContainer
        Layout.fillWidth: true
        // height: _input.implicitHeight + 12
        height: pysize.edit_height
        border.width: _input.activeFocus ? 2 : 0
        border.color: root.outlineColor
        color: root.color
        radius: pysize.radius_l

        Behavior on border.width {
            NumberAnimation {
                duration: 100
            }
        }

        SequentialAnimation {
            id: _borderColorAnimation
            // running: false
            ColorAnimation {
                target: _inputContainer
                property: 'border.color'
                to: pycolor.theme_blue
                duration: 100
            }
            ColorAnimation {
                target: _inputContainer
                property: 'border.color'
                to: root.outlineColor
                duration: 200
            }
        }

        MouseArea {
            anchors.fill: parent
            cursorShape: root.enabled ? Qt.IBeamCursor : Qt.ForbiddenCursor
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
            color: root.enabled ? pycolor.on_surface : pycolor.outline
            enabled: root.enabled
            font.family: pyfont.font_default
            font.pixelSize: pyfont.size_m
            readOnly: root.readonly
            selectionColor: pycolor.primary
            text: root.text

            onEditingFinished: {
                if (root._userEdited) {
                    root.editingFinished(root.text)
                    root._userEdited = false
                }
            }
            onTextChanged: {
                root.text = text
                root._userEdited = true
            }

            Text {
                visible: root.placeholder && !root._hasContent
                anchors.fill: parent
                verticalAlignment: Q.TextInput.AlignVCenter
                font: parent.font
                opacity: 0.5
                text: root.placeholder
            }
        }

        Component.onCompleted: {
            root.editingFinished.connect(() => {
                if (_input.activeFocus) {
                    _borderColorAnimation.start()
                }
            })
        }
    }

    Item {
        visible: root.showEditingHint
        Layout.fillWidth: true
        Layout.preferredHeight: pysize.below_entry_height

        property string _lastEditedText

        Text {
            visible: (
                root.enabled &&
                root._hasContent &&
                _input.activeFocus &&
                root.text != parent._lastEditedText
            )
            anchors {
                right: parent.right
                rightMargin: 2
                verticalCenter: parent.verticalCenter
            }
            font.pixelSize: pyfont.size_s
            text: 'Press Enter to apply'
        }

        Component.onCompleted: {
            this._lastEditedText = root.text
            root.editingFinished.connect((text) => this._lastEditedText = text)
        }
    }
}
