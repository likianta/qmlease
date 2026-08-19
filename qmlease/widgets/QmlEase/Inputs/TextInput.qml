import QtQuick
import QtQuick as Q
import "../Controls" as C
import "../Layouts" as L
import "../Visual" as V

L.Column {
    id: root
    implicitWidth: 200

    property string color: pycolor.container
    property string help: ''
    property alias  inputMask: inputBox.inputMask
    property alias  inputWidth: inputBox.width
    property string label: ''
    property string outlineColor: pycolor.outline
    property string placeholder: ''
    property string prefix: ''
    property bool   readonly: false
    property bool   showEditingHint: false
    property alias  text: inputBox.text
    property string textColor: pycolor.on_container
    property bool   _hasContent: text.length > 0
    property bool   _userEdited: false

    signal editing(string text)
    signal editingFinished(string text)

    // header row (above input box)
    Item {
        visible: root.label || root.help
        width: parent.width
        height: 16

        V.Text {
            id: label
            anchors {
                left: parent.left
                leftMargin: 2
                verticalCenter: parent.verticalCenter
            }
            color: root.enabled ? pycolor.text_primary : pycolor.text_secondary
            text: root.label
        }

        // TODO: root.help icon
    }

    V.Rectangle {
        id: inputContainer
        width: parent.width
        height: 36
        border.width: inputBox.activeFocus ? 2 : 0
        border.color: root.outlineColor
        color: root.color

        Behavior on border.width {
            NumberAnimation {
                duration: 100
            }
        }

        // border breathing effect, will be triggered when user presses enter to 
        // submit something.
        SequentialAnimation {
            id: borderBreathingEffect
            ColorAnimation {
                target: inputContainer
                property: 'border.color'
                to: pycolor.solid_brand
                duration: 100
            }
            ColorAnimation {
                target: inputContainer
                property: 'border.color'
                to: root.outlineColor
                duration: 200
            }
        }

        L.Row {
            id: inputRow
            anchors.fill: parent
            valign: 'center'
            hpadding: 8
            spacing: 2
                
            V.Text {
                visible: root.prefix
                text: root.prefix
                color: pycolor.text_dim
            }

            Q.TextInput {
                id: inputBox
                enabled: root.enabled
                clip: true
                color: root.enabled ? root.textColor : pycolor.text_secondary
                font.pixelSize: 12
                readOnly: root.readonly
                selectionColor: pycolor.solid_brand
                // text: root.text

                onEditingFinished: {
                    if (root._userEdited) {
                        root.editingFinished(root.text)
                        root._userEdited = false
                    }
                }

                // onTextChanged: {
                //     // root.text = text
                //     root._userEdited = true
                // }

                onTextEdited: {
                    root.editing(root.text)
                    root._userEdited = true
                }

                // placeholder
                V.Text {
                    visible: root.placeholder && !root._hasContent
                    anchors.fill: parent
                    color: inputBox.color
                    font: parent.font
                    opacity: 0.5
                    text: root.placeholder
                    verticalAlignment: Q.TextInput.AlignVCenter
                    wrapMode: Text.NoWrap
                }
            }
        }

        // just changes hovering cursor shape.
        C.MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.NoButton
            // cursorShape: root.enabled ? Qt.IBeamCursor : Qt.ForbiddenCursor
            // cursorShape: root.readonly ? Qt.ArrowCursor : Qt.IBeamCursor
            cursorShape:
                root.enabled ?
                (root.readonly ? Qt.ArrowCursor : Qt.IBeamCursor) :
                Qt.ForbiddenCursor
        }
    }

    // footer (below input box)
    Item {
        width: parent.width
        implicitHeight: hint.implicitHeight
        visible: root.showEditingHint

        property string _lastEditedText

        V.Text {
            id: hint
            visible: (
                root.enabled &&
                root._hasContent &&
                inputBox.activeFocus &&
                root.text != parent._lastEditedText
            )
            anchors {
                right: parent.right
                rightMargin: 2
                verticalCenter: parent.verticalCenter
            }
            font.pixelSize: 11
            text: 'Press Enter to apply'
        }

        Component.onCompleted: {
            this._lastEditedText = root.text
            root.editingFinished.connect(
                (text) => { this._lastEditedText = text }
            )
        }
    }

    Component.onCompleted: {
        root.editingFinished.connect(() => {
            if (inputBox.activeFocus) {
                borderBreathingEffect.start()
            }
        })
    }
}
