import QtQuick

Rectangle {
    width: pysize.wrap
    height: pysize.wrap
    border.color: mouseEntered ? borderColor1 : borderColor0
    color: mouseEntered ? color1 : color0
    radius: pysize.radius_m

    property string alignment: 'center'
    property string borderColor0: 'transparent'
    property string borderColor1: pycolor.border_default
    property string color0: 'transparent'
    property string color1: 'transparent'
    property alias  mouseEntered: _area.containsMouse
    property alias  mousePressed: _area.pressed
    property var    padding: [pysize.padding_v_m, pysize.padding_h_l]
    property var    targetChild: null

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: true
    }

    Component.onCompleted: {
        py.qmlease.widget.init_ghost_border(this)
    }
}
