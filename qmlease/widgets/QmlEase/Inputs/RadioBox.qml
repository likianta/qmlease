import QtQuick
import QtQuick.Layouts
import QmlEase

Rectangle {
    id: root
    width: _option.width + _leftPadding + _rightPadding
    height: pysize.entry_height_s
    border.width: ghostBorder && _area.containsMouse ? 1 : 0
    color: pycolor.transparent

    property bool   checked
    property bool   ghostBorder
    property string text
    property int    _leftPadding: ghostBorder ? 4 : 0
    property int    _rightPadding: ghostBorder ? 12 : 0

    signal clicked()

    RowLayout {
        id: _option
        x: parent._leftPadding
        height: parent.height
        spacing: pysize.spacing_s

        // indicator
        Rectangle {
            Layout.alignment: Qt.AlignVCenter
            width: height
            height: pysize.indicator_size
            radius: height / 2
            border.width: root.checked ? 1 : 2
            border.color: pycolor.secondary
            clip: true
            color: pycolor.transparent

            Rectangle {
                anchors.centerIn: parent
                width: height
                height: root.checked ? parent.height - 6 : 0
                radius: height / 2
                color: pycolor.secondary

                Behavior on height {
                    NumberAnimation {
                        duration: 200
                        easing.overshoot: 1.5
                        easing.type: Easing.OutBack
                    }
                }
            }
        }

        Text {
            Layout.alignment: Qt.AlignVCenter
            text: root.text
        }
    }

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: root.ghostBorder
        onClicked: root.clicked()
    }
    
    // Component.onCompleted: {
    //     py.qmlease.inspect_size(this, `RadioBox:${root.text}`)
    // }
}
