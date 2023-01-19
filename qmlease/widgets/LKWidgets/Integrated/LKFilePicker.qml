import QtQuick 2.15
import ".."

LKRow {
    width: pysize.bar_width
    height: pysize.bar_height
    alignment: 'vcenter'
//    autoSize: true

    property string defaultPath
    property string label
    property alias  labelItem: _label
    property string filter: ''
    //  e.g. 'Image Files (*.png *.jpg *.bmp)'
    //    or 'Images (*.png *.xpm *.jpg);;Text files (*.txt);;XML files (*.xml)'
    property string ftype: 'file'  // literal['file', 'folder']
    property alias  path: _input.text

    LKText {
        id: _label
        visible: Boolean(parent.label)
        horizontalAlignment: Text.AlignRight
        text: parent.label
    }

    LKInput {
        id: _input
//        width: pyenum.STRETCH
        width: _label.visible ?
            parent.width - _btn.width - parent.spacing * 2 - _label.width :
            parent.width - _btn.width - parent.spacing
        height: parent.height
        textHint: parent.defaultPath
    }

    LKButton {
        id: _btn
        width: pysize.button_width_l
        height: parent.height
        text: 'Browse'
        onClicked: {
            const path = lkutil.file_dialog({
                'type_': parent.ftype,
                'type_filter': parent.filter,
            })
            if (path) {
                _input.text = path
            }
        }
    }
}



