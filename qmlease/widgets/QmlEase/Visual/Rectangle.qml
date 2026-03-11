/// the minimal rectangle imple with a predefined radius.
import QtQuick

Rectangle {
    border.width: 0
    border.color: pycolor.border_default
    clip: true
    color: pycolor.white
    radius: pysize.radius_m
}
