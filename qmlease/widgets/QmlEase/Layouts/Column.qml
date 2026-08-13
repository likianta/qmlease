/// Note: This file is a simple copy-paste from Row.qml, but with Column instead 
/// of Row for `id: realContainer`.

import QtQuick as Q
import QmlEase as E

Q.Item {
    id: root
    clip: true
    implicitWidth: realContainer.implicitWidth + borderWidth * 2
    implicitHeight: realContainer.implicitHeight + borderWidth * 2

    default property alias content: realContainer.data

    property bool   border: false // shorthand for borderWidth
    property bool   borderColor: pycolor.outline
    property int    borderWidth: border ? 1 : 0
    property string color: pycolor.transparent
    property int    spacing: 4

    E.Rectangle {
        anchors.fill: parent
        border.width: root.borderWidth
        border.color: root.borderColor
        color: root.color

        Q.Column {
            id: realContainer
            anchors {
                fill: parent
                margins: root.borderWidth
            }
            spacing: root.spacing
        }
    }

    // Q.Component.onCompleted: {
    //     py.qmlease.inspect_size(this, 'row layout')
    //     py.qmlease.inspect_size(realContainer, 'inner row layout')
    // }
}
