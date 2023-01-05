import QtQuick 2.0
import QtQuick.Controls 2.0

Button {
    // https://stackoverflow.com/questions/15236304/need-to-change-color-of
    //  -an-svg-image-in-qml
    id: root

    enabled: false
    background: Item {}
    flat: true
    hoverEnabled: false
    icon.width: root.size
    icon.height: root.size
    icon.color: root.color
    icon.source: root.source

    property string color: pycolor.icon_line_default
    property alias  hovered_: _area.containsMouse
    property int    size: pysize.icon_size
    property string source

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: true
        onClicked: (mouse) => root.clicked(mouse)
    }
}
