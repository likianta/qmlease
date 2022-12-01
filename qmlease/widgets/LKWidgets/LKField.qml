import QtQuick 2.15

Item {
    id: root
    width: pysize.field_width
    height: pysize.field_height
    clip: true

    property Component delegate: LKInput { }
    property alias     fieldItem: _loader.item
    property int       spacing: pysize.spacing_l
    property alias     text: _text.text
    property alias     textItem: _text
    property int       widthA: 0
    property int       widthB: 0

    LKText {
        id: _text
//        visible: Boolean(text)
        anchors {
//            left: parent.left
//            right: _loader.left
//            rightMargin: root.spacing
            verticalCenter: parent.verticalCenter
        }
        width: root.widthA
        clip: true
        horizontalAlignment: Text.AlignRight
    }

    Loader {
        id: _loader
        anchors {
            right: parent.right
            verticalCenter: parent.verticalCenter
        }
        width: root.widthB
//        height: root.height
        sourceComponent: root.delegate
        onLoaded: {
            this.item.width = Qt.binding(() => this.width)
        }
    }

    Component.onCompleted: {
        if (this.widthA && this.widthB) {
            root.width = this.widthA + this.widthB + root.spacing
        } else if (this.widthA && !this.widthB) {
            this.widthB = Qt.binding(() => {
                return root.width - this.widthA - root.spacing
            })
        } else if (!this.widthA && this.widthB) {
            this.widthA = Qt.binding(() => {
                return root.width - this.widthB - root.spacing
            })
        } else {
            this.widthA = Qt.binding(() => {
                return pylayout.calc_content_width(_text.text)
            })
            this.widthB = Qt.binding(() => {
                if (this.widthA == 0) {
                    return root.width
                } else {
                    return root.width - this.widthA - root.spacing
                }
            })
        }
    }
}
