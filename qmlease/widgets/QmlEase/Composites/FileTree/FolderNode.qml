import QtQuick
import QmlEase

GhostBorder {
    id: root
    border.color: (mouseEntered || _icon.hovered) ?  borderColor1 : borderColor0
    padding: [4, 20, 4, 4]

    property bool   checkable: false
    property bool   checked: false
    property alias  expanded: _icon.state_
    property bool   selected: false
    property string text: ''

    onClicked: {
        // console.log('FolderNode clicked')
        this.checked = !this.checked
        this.selected = true
    }

    Row {
        spacing: checkable ? 2 : 4
        IconButton {
            id: _icon
            halo: true
//            source0: pyassets.get('qmlease', 'arrow-right-s-line.svg')
//            source1: pyassets.get('qmlease', 'arrow-down-s-line.svg')
            source: pyassets.get('qmlease', 'arrow-right-s-line.svg')
            rotation: state_ ? 90 : 0
            // onClicked: {
            //     console.log('FolderNode icon clicked')
            // }
            Behavior on rotation {
                NumberAnimation {
                    duration: 60
                }
            }
        }
        CheckBox {
            id: _chk
            visible: root.checkable
        }
        Text {
            text: root.text
        }
    }
}
