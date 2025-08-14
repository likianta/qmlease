import QtQuick
import QtQuick.Controls

Button {
    // https://stackoverflow.com/questions/15236304/need-to-change-color-of
    //  -an-svg-image-in-qml
    enabled: false
    background: Item {}
    flat: true
    hoverEnabled: false
    icon.width: size
    icon.height: size
    icon.color: color
    icon.source: source

    property string color: pycolor.icon_line_default
    property alias  hovering: _area.containsMouse
    property int    size: pysize.icon_size
    property string source

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: true
        onClicked: (mouse) => parent.clicked(mouse)
    }
}
