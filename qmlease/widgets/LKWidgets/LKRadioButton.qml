import QtQuick

Rectangle {
    id: root
    width: radius * 2
    height: radius * 2
    radius: pysize.indicator_radius

    border.width: checked ? radius : (hovered ? 2 : 1)
    border.color: (checked || hovered) ?
        pycolor.border_active : pycolor.border_inactive

    property bool   hovered: _area.containsMouse
    property bool   checked: false
    property string icon: ''
    property alias  text: _text.text

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: true
    }

    LKRow {
        anchors {
            left: parent.left
            verticalCenter: parent.verticalCenter
        }
        spacing: pysize.spacing_s

        Loader {
            onLoaded: {
                this.width = this.item.width
                this.height = this.item.height
            }
            Component.onCompleted: {
                if (root.icon) {
                    this.source = root.icon
                }
            }
        }

        LKText {
            id: _text
        }
    }

    Behavior on border.width {
        NumberAnimation {
            duration: pymotion.duration
            easing.type: Easing.OutQuad
        }
    }

    Behavior on border.color {
        ColorAnimation {
            duration: pymotion.duration
        }
    }
}
