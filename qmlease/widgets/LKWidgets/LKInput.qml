import QtQuick 2.15
import QtQuick.Controls 2.15

LKRectangle {
    id: root
    width: pysize.edit_width
    height: pysize.edit_height
    border.width: 1
    border.color: _input.activeFocus ? borderColorActive : borderColor
    color: _input.activeFocus ? bgColorActive : bgColor

    readonly property alias inputItem: _input

    property string bgColor: pycolor.input_bg_default
    property string bgColorActive: pycolor.input_bg_active
    property string borderColor: pycolor.input_border_default
    property string borderColorActive: pycolor.input_border_active
    property string bottomColorHighlight: pycolor.input_indicator_active
    property string cursorColor: pyenum.DEFAULT
    property string textColor: pycolor.text_default

    property alias  displayText: _input.displayText
    property bool   editable: true
    property alias  horizontalAlignment: _input.horizontalAlignment
    property alias  inputMask: _input.inputMask
    property int    padding: pysize.padding_l
    property bool   pressEscToLostFocus: false  // TODO
    property bool   showIndicator: false
    property alias  text: _input.text
    property alias  textHint: _placeholder.text
    property bool   useIBeamCursor: true
    property alias  validator: _input.validator

    signal submit(string text)
    signal textEdited(string text)

    function activate() {
        _input.forceActiveFocus()
    }

    MouseArea {
        id: _cursor_shape_patch
        visible: root.useIBeamCursor
        anchors.fill: parent
        acceptedButtons: Qt.NoButton
        cursorShape: Qt.IBeamCursor
    }

    LKText {
        id: _placeholder
        visible: _placeholder.text && !_input.text
        anchors {
            left: parent.left
            right: parent.right
            leftMargin: root.padding
            rightMargin: root.padding
            verticalCenter: parent.verticalCenter
        }
        color: pycolor.text_hint
        // TODO: font binds to _input.font
    }

    TextInput {
        id: _input
        enabled: root.editable
        anchors.fill: _placeholder
        clip: true
        color: root.textColor
        font.family: pyfont.font_default
        font.pixelSize: pyfont.size_m
        selectByMouse: true

        onTextEdited: {
//            console.log(this.text, this.displayText)
            root.textEdited(this.text)
        }

        onEditingFinished: {
            root.submit(this.text)
        }

        Component {
            id: _custom_cursor

            Rectangle {
                // https://stackoverflow.com/questions/58719796/qml-change
                //  -cursor-color-in-textfield
                id: _custom_cursor_rect
                visible: false
                width: _input.cursorRectangle.width
                height: _input.height - 2
                color: root.cursorColor

                SequentialAnimation {
                    loops: Animation.Infinite
                    running: _input.cursorVisible

                    PropertyAction {
                        target: _custom_cursor_rect
                        property: 'visible'
                        value: true
                    }

                    PauseAnimation {
                        duration: 600
                    }

                    PropertyAction {
                        target: _custom_cursor_rect
                        property: 'visible'
                        value: false
                    }

                    PauseAnimation {
                        duration: 600
                    }

                    onStopped: {
                        _custom_cursor_rect.visible = false
                    }
                }
            }
        }

        Component.onCompleted: {
            if (root.cursorColor != pyenum.DEFAULT) {
                _input.cursorDelegate = _custom_cursor
            }
        }
    }

    Rectangle {
        id: _bottom_highlight
        visible: root.showIndicator
        anchors.bottom: parent.bottom
//        anchors.bottomMargin: 1
        anchors.horizontalCenter: parent.horizontalCenter
        width: parent.width - 2
        height: _input.activeFocus ? 2 : 0
        radius: parent.radius
        color: root.bottomColorHighlight
    }
}
