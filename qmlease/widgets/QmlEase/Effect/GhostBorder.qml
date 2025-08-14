import QtQuick

Rectangle {
    width: pysize.wrap
    height: pysize.wrap
    border.color: (
        active ? (mouseEntered ? borderColor1 : borderColor0) : borderColor0
    )
    color: active ? (mouseEntered ? color1 : color0) : color0
    radius: pysize.radius_m

    property bool   active: true
    property string borderColor0: 'transparent'
    property string borderColor1: pycolor.border_default
    property string color0: 'transparent'
    property string color1: 'transparent'
    property alias  mouseEntered: _area.containsMouse
    property alias  mousePressed: _area.pressed
    property var    padding: [pysize.padding_v_m, pysize.padding_h_l]

    signal clicked()

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: true
        // propagateComposedEvents: true
        onClicked: (evt) => {
            // console.log('GhostBorder clicked')
            parent.clicked()
            // evt.accepted = false
        }
    }

    Component.onCompleted: {
        py.qmlease.widget.init_ghost_border(this)
    }
}
