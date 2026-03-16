import QtQuick
import QmlEase

Rectangle {
    width: pysize.indicator_size_l
    height: pysize.indicator_size_l
    border.width: 1
    color: pycolor.transparent
    radius: pysize.radius_m

    property bool checked

    Image {
        visible: parent.checked
        anchors {
            fill: parent
            margins: 2
        }
        fillMode: Image.PreserveAspectFit
        source: './Assets/check.svg'
    }
}
