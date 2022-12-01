import QtQuick

Image {
    id: root
    width: p_size
    height: p_size

    property int    p_size: root.sourceSize.width
    property alias  p_source: root.source
}