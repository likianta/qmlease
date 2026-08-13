/// the minimal rectangle imple with a predefined radius.
import QtQuick

Rectangle {
    border.width: 0
    border.color: pycolor.outline
    clip: true
    color: pycolor.transparent
    radius: pysize.radius_l
}
