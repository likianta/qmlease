import QtQuick 2.15

LKRectangle {
    id: root
    width: pysize.edit_width
    height: pysize.edit_height
    border.width: 1
    border.color: _input.activeFocus ? colorBorderActive : colorBorderDefault
    color: _input.activeFocus ? colorBgActive : colorBgDefault

    property string colorBgDefault: pycolor.input_bg_default
    property string colorBgActive: pycolor.input_bg_active
    property string colorBorderDefault: pycolor.input_border_default
    property string colorBorderActive: pycolor.input_border_active
    property string colorBottomHighlight: pycolor.input_indicator_active
    property alias  displayText: _input.displayText
    property bool   editable: true
    property alias  horizontalAlignment: _input.horizontalAlignment
    property alias  inputItem: _input
    property alias  inputMask: _input.inputMask
    property int    padding: pysize.padding_l
    property bool   pressEscToLostFocus: false  // TODO
    property bool   showIndicator: false
//    property bool   showIndicator: Boolean(colorBottomHighlight)
    property alias  text: _input.text
    property alias  textColor: _input.color
    property alias  textHint: _placeholder.text
    property bool   useIBeamCursor: false
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
        color: pycolor.text_default
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
        color: root.colorBottomHighlight
    }
}
