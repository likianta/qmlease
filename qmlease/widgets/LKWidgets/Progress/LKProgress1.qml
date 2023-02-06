// the simplest progress bar with no number indicator.
import QtQuick 2.15

BaseControl {
    id: root
    width: pysize.progress_width
    height: pysize.progress_height

    property string colorBg: pycolor.progress_bg
    property string colorFg: pycolor.progress_fg
    property alias  innerHeight: _prog_fg.height

    Rectangle {
        id: _prog_bg
        width: parent.width
        height: parent.height
        radius: pysize.progress_radius
        color: root.colorBg

        Rectangle {
            id: _prog_fg
            anchors {
                left: parent.left
                verticalCenter: parent.verticalCenter
            }
            width: _fullWidth * _percentage
            height: pysize.progress_inner_height
            radius: parent.radius
            color: root.colorFg

            property int  _fullWidth: parent.width - pysize.padding_s * 2
            property real _percentage: root._value
        }
    }
}
