import QtQuick 2.15
import QtQuick.Controls 2.15
import "Buttons"

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
    property string textColor: pycolor.text_main

    property alias  displayText: _input.displayText
    property bool   editable: true
    property alias  horizontalAlignment: _input.horizontalAlignment
    property alias  inputMask: _input.inputMask
    property int    padding: pysize.padding_l
    property bool   pressEscToLostFocus: false  // TODO
    property bool   showClearButton: false
    property bool   showIndicator: false
    property alias  text: _input.text
    property alias  textHint: _placeholder.text
    property bool   useIBeamCursor: true
    property alias  validator: _input.validator

    signal clicked()
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

    Item {
        id: _input_container
        anchors.fill: _placeholder
        clip: true

        TextInput {
            id: _input
            enabled: root.editable
            anchors {
                left: parent.left
                right: _clear_button.left
                top: parent.top
                bottom: parent.bottom
                leftMargin: 4
            }
            clip: true
            color: root.textColor
            font.family: pyfont.font_default
            font.pixelSize: pyfont.size_m
            selectByMouse: true

            onActiveFocusChanged: {
                if (this.activeFocus) {
                    root.clicked()
                }
            }

            onTextEdited: {
                root.textEdited(this.text)
            }

            onAccepted: {
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

        LKIconButton {
            id: _clear_button
            visible: root.showClearButton
            anchors {
                right: parent.right
                verticalCenter: parent.verticalCenter
                margins: 4
            }
            halo: true
            opacity: _input.displayText ? 1 : 0
            source: pyassets.get('lkwidgets', 'Assets/close-line.svg')

            onClicked: {
                _input.text = ''
            }

            Behavior on opacity {
                NumberAnimation {
                    duration: 200
                }
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
