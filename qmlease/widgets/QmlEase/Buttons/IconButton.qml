import QtQuick
import QtQuick.Controls

Item {
    id: root
    width: size * 1.5
    height: size * 1.5
    clip: false

    property string bgColor: pycolor.primary_container
    property string color: pycolor.on_primary_container
    property alias  cursorShape: _area.cursorShape
    property bool   halo: false
    property alias  hovered: _area.containsMouse
    property alias  icon: _btn.icon
    property int    size: pysize.icon_size
    property string source
    property string source0
    property string source1
    property bool   state_: false
    // property bool   __stateful: source0 && source1

    // signal clicked(var mouse)
    signal clicked(bool active)

//    function activate() {
//        root.state_ = true
//        if (root.__stateful) {
//            root.source = root.source1
//        }
//    }
//
//    function reset() {
//        root.state_ = false
//        if (root.__stateful) {
//            root.source = root.source0
//        }
//    }

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
        onClicked: {
            root.state_ = !root.state_
            root.clicked(root.state_)
        }
    }

    Component.onCompleted: {
        if (this.source0 && this.source1) {
            this.source = Qt.binding(() => {
                return this.state_ ? this.source1 : this.source0
            })
        }
    }
}
