import QtQuick 2.15
import QtQuick.Controls 2.15
import "./LCBackground"
import "./LCStyle/dimension.js" as LCDimension
import "./LCStyle/motion.js" as LCMotion
import "./LCStyle/palette.js" as LCPalette
import "./LCStyle/typography.js" as LCTypo

Item {
    id: root
    implicitWidth: LCDimension.BarWidth
    implicitHeight: LCDimension.BarHeight

    property alias p_active: _field.activeFocus
    property alias p_alignment: _field.p_alignment
    property bool  p_bold: false
    property alias p_field: _field
    property alias p_hint: _field.placeholderText
    property alias p_title: _title.p_text
    property alias p_value: _field.text

    signal clicked()

    LCText {
        id: _title
        anchors {
            left: parent.left
            verticalCenter: parent.verticalCenter
        }
        width: _title.implicitWidth
        rightPadding: _title.text == '' ? 0 : LCDimension.PaddingM
        p_alignment: 'rcenter'
        p_bold: parent.p_bold
    }

    TextField {
        id: _field
        anchors {
            left: _title.right
            right: parent.right
            verticalCenter: parent.verticalCenter
        }
        height: parent.height
        leftPadding: LCDimension.HSpacingM; rightPadding: LCDimension.HSpacingM
        topPadding: 0; bottomPadding: 0

        font.bold: parent.p_bold
        font.pixelSize: LCTypo.FontSizeM
        placeholderTextColor: LCPalette.TextHint
        selectByMouse: true
        selectedTextColor: LCPalette.TextSelected
        selectionColor: LCPalette.TextSelection

        property string p_alignment: 'lcenter'

        background: LCFieldBg {
            p_active: root.p_active
        }

        Component.onCompleted: {
            this.cursorPosition = 0
            this.pressed.connect(root.clicked)
            LKLayoutHelper.quick_align(this, p_alignment)
        }
    }
}
