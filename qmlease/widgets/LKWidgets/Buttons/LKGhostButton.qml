import QtQuick 2.15
import ".."

LKRectangle {
    id: root
    width: 0
    height: 0
    radius: pysize.button_radius
    border.width: hovered ? 1 : 0
    border.color: borderColor
    color: selected ? bgActive : (hovered ? bgHovered : 'transparent')

    readonly property alias textItem: _text

    property string bgHovered: pycolor.button_bg_hovered
    property string bgActive: pycolor.button_bg_active
    property string borderColor: pycolor.border_glow
    property alias  hovered: _area.containsMouse
    property string iconColor
    property var    iconDelegate
    property int    iconSize: pysize.icon_size
    property string iconSource
    property bool   selected: false
    property string text

    signal clicked()

    Loader {
        id: _icon_loader
        enabled: Boolean(root.iconSource)
        anchors {
            left: parent.left
            leftMargin: pysize.padding_h_m
            verticalCenter: parent.verticalCenter
        }
//        width: root.iconSize
//        height: root.iconSize
        sourceComponent: LKIconButton { }
        onLoaded: {
            this.item.color = root.iconColor
            this.item.size = root.iconSize
            this.item.source = root.iconSource
            root.iconDelegate = this.item
        }
    }

    LKText {
        id: _text
        anchors.fill: parent
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        text: root.text

        Component.onCompleted: {
            if (root.iconSource) {
                this.horizontalAlignment = Text.AlignLeft
                this.leftPadding = _icon_loader.x
                    + _icon_loader.width
                    + pysize.padding_h_m
            }
        }
    }

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: true
        onClicked: root.clicked()
    }

    Component.onCompleted: {
        if (this.width == 0) {
            this.width = _text.contentWidth * 1.5
        }
        if (this.height == 0) {
            this.height = _text.contentHeight * 1.5
        }
    }
}
