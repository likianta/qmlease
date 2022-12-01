import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: root
    width: size * 1.5
    height: size * 1.5
    clip: false

    property string bgColor: pycolor.button_bg_hovered
    property string color
    property alias  cursorShape: _area.cursorShape
    property bool   halo: false
    property alias  hovered: _area.containsMouse
    property alias  icon: _btn.icon
    property int    size: pysize.icon_size
    property string source

    signal clicked(var mouse)

    Rectangle {
        visible: root.halo
        anchors.centerIn: parent
        width: root.size * 1.5
        height: root.size * 1.5
        radius: height / 2
        color: root.bgColor
        opacity: root.hovered ? 1 : 0
        Behavior on opacity {
            NumberAnimation {
                duration: 100
            }
        }
    }

    Button {
        // https://stackoverflow.com/questions/15236304/need-to-change-color-of
        //  -an-svg-image-in-qml
        id: _btn
        enabled: false
        anchors.centerIn: parent
        background: Item {}
        flat: true
        hoverEnabled: false
        icon.width: root.size
        icon.height: root.size
        icon.color: root.color
        icon.source: root.source
    }

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: true
        onClicked: (mouse) => root.clicked(mouse)
    }
}
