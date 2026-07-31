import QtQuick
import QmlEase as QE

QE.Rectangle {
    id: root
    width: 0
    height: pysize.button_height
    border.width: ghostBorder ? (_area.containsMouse ? 1 : 0) : 0
    border.color: pycolor.outline
    color: (
        _area.containsPress ? colorBgPressed :
        _area.containsMouse ? colorBgHovered :
        pycolor.transparent
    )

    property bool   checkable: true
    property bool   checked: false
    property string colorBgHovered: 'transparent'
    property string colorBgPressed: pycolor.container_tint
    property bool   ghostBorder: false
    property int    indicatorSize: pysize.indicator_size
    property string text: ''
    property alias  textItem: _text
    property int    __padding: pysize.padding_m

    signal toggled(bool checked)

    QE.Rectangle {
        id: _indicator
        anchors {
            left: parent.left
            leftMargin: root.__padding
            verticalCenter: parent.verticalCenter
        }
        width: root.indicatorSize
        height: root.indicatorSize
        border.width: 1
        border.color: pycolor.outline
        color: pycolor.transparent

        Image {
            visible: root.checked
            anchors {
                fill: parent
                margins: 1
            }
            source: '../Assets/check.svg'
        }
    }

    QE.Text {
        id: _text
        anchors {
            left: _indicator.right
            leftMargin: root.__padding
            verticalCenter: parent.verticalCenter
        }
        color: root.checkable ? pycolor.text_main : pycolor.text_dim
        text: root.text
    }

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: true
        onClicked: {
            if (root.checkable) {
                root.checked = !root.checked
                root.toggled(root.checked)
            }
        }
    }

    Component.onCompleted: {
        if (this.width == 0) {
            if (this.text) {
                this.width = this.childrenRect.width * 1.5
            } else {
                this.width = this.childrenRect.width
            }
        }
    }
}
