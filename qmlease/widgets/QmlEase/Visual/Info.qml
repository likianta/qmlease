// ref: https://daisyui.com/components/alert/
import QtQuick
import QmlEase

Rectangle {
    id: root
    implicitWidth: _text.implicitWidth + _hpadding * 2
    implicitHeight: _text.implicitHeight + _vpadding * 2
    border.width: 2
    border.color: pycolor.get(_accentColor, 'border')
    color: type == 'error' ? 
        pycolor.error_container : pycolor.get(_accentColor, 'container')

    property string text
    property string type: 'info'
    property string _accentColor: (
        type == 'error' ? pycolor.error : 
        type == 'info' ? pycolor.theme_blue : 
        type == 'success' ? pycolor.theme_green : 
        type == 'warning' ? pycolor.theme_yellow : 
        pycolor.surface_container
    )
    property int    _hpadding: pysize.padding_xl
    property int    _vpadding: pysize.padding_l

    Text {
        id: _text
        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            right: parent.right
            leftMargin: _hpadding
            rightMargin: _hpadding
            // topMargin: _vpadding
            // bottomMargin: _vpadding
        }
        // color: pycolor.on_surface
        color: pycolor.get(root.color, 'on')
        text: root.text
    }
}
