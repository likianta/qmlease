import QtQuick
import QmlEase

Rectangle {
    property bool checked
    width: pysize.indicator_size
    height: pysize.indicator_size
    // TODO
    color: checked ? pycolor.primary : pycolor.transparent
}
