import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: root
    width: size * 1.5
    height: size * 1.5
    clip: false

    property bool   active_: false
    property string bgColor: pycolor.button_bg_hovered
    property string color: pycolor.icon_line_default
    property alias  cursorShape: _area.cursorShape
    property bool   halo: false
    property alias  hovered: _area.containsMouse
    property alias  icon: _btn.icon
    property int    size: pysize.icon_size
    property string source
    property string source0
    property string source1
    // property bool   __stateful: source0 && source1

    // signal clicked(var mouse)
    signal clicked(bool active)

//    function activate() {
//        root.active_ = true
//        if (root.__stateful) {
//            root.source = root.source1
//        }
//    }
//
//    function reset() {
//        root.active_ = false
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
            root.active_ = !root.active_
            root.clicked(root.active_)
        }
    }

    Component.onCompleted: {
        if (this.source0 && this.source1) {
            this.source = Qt.binding(() => {
                return this.active_ ? this.source1 : this.source0
            })
        }
    }
}
