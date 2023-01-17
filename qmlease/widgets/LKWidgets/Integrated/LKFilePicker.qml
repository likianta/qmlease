import QtQuick 2.15
import ".."

LKRow {
    width: pysize.bar_width
    height: pysize.bar_height
    alignment: 'vcenter'
    autoSize: true

    property string defaultPath
    property string field
    property alias  fieldItem: _label
    property string filter: ''
    //  e.g. 'Image Files (*.png *.jpg *.bmp)'
    //    or 'Images (*.png *.xpm *.jpg);;Text files (*.txt);;XML files (*.xml)'
    property string ftype: 'file'  // literal['file', 'folder']
    property alias  path: _input.text

    LKText {
        id: _label
        visible: Boolean(parent.field)
        horizontalAlignment: Text.AlignRight
        text: parent.field
    }

    LKInput {
        id: _input
        width: pyenum.STRETCH
        height: parent.height
        textHint: parent.defaultPath
    }

    LKButton {
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



