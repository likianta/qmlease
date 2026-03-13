import QtQuick
import QtQuick.Layouts
import QmlEase

Item {
    id: root
    width: _option.width
    height: _option.height

    property bool checked
    signal clicked()

    RowLayout {
        id: _option
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
            text: modelData
        }
    }

    MouseArea {
        anchors.fill: parent
        onClicked: root.clicked()
    }
}
