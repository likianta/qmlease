// https://chatgpt.com/share/6a7d44ad-ae44-83e9-b929-8359fd249e1a

import QtQuick
import QtQuick.Controls.impl // caution: internal API
// import QtQuick.Effects

Item {
    id: root
    width: halo ? _haloSize : _iconSize
    height: halo ? _haloSize : _iconSize
    clip: true

    property string color: pycolor.paint_brand
    property int    fineTuneSizeOffset: 0
    //  if different icons with same size but not look equally large, use this
    //  to fine tune the icon size.
    //  suggest giving 0, 1, 2, -1, -2 as values.
    //  ref: https://chatgpt.com/share/6a7d5a68-403c-83ee-896d-efcb3ef18204
    property bool   halo: false
    property int    size: 16
    property string source
    property int    _haloSize: size + 4
    property int    _iconSize: size + fineTuneSizeOffset
    // property int    _padding: halo ? 2 : 0

    Rectangle {
        visible: root.halo
        anchors.fill: parent
        radius: width / 2
        color: mouse.containsMouse ? 
            pycolor.container_tint : pycolor.transparent
        MouseArea {
            id: mouse
            anchors.fill: parent
            hoverEnabled: true
        }
    }
    
    // https://doc.qt.io/qt-6/qml-qtquick-effects-multieffect.html
    // notice: if source is svg image, you must ensure the `fill` attribute is
    // set to "white", otherwise the colorization will not work. (ref:
    // https://forum.qt.io/post/753574)
    // Image {
    //     // id: img
    //     // visible: false
    //     anchors.centerIn: parent
    //     width: root._iconSize
    //     height: root._iconSize
    //     layer.enabled: true
    //     layer.effect: MultiEffect {
    //         colorization: 1.0
    //         colorizationColor: root.color
    //     }
    //     source: root.source
    //     sourceSize.width: root._iconSize
    //     sourceSize.height: root._iconSize
    // }

    IconImage {
        anchors.centerIn: parent
        width: root._iconSize
        height: root._iconSize
        color: root.color
        source: root.source
        sourceSize.width: root._iconSize
        sourceSize.height: root._iconSize
    }
}
