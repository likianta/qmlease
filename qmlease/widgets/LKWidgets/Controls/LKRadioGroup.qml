import QtQuick 2.15
import ".."  // for LKText
import "../Buttons"  // for LKRadioBox
import "../Layouts"  // for LKRow

LKRow {
    id: root

    property int    currentIndex  // readonly
    property string currentItem  // readonly
    property int    index: 0
    property string label
    property alias  labelItem: _label
    property var    options  // list[str]
    property bool   showGhostBorder: false

    signal checked(int index, string label)

    LKText {
        id: _label
        text: root.label
    }

    Repeater {
        model: root.options.length
        delegate: LKRadioBox {
            height: root.height
            showGhostBorder: root.showGhostBorder
            text: root.options[index]

            property int index: model.index

            Component.onCompleted: {
                if (this.index == root.index) {
                    this.checked = true
                }
                this.onToggled.connect(() => {
                    root.currentIndex = this.index
                    root.currentItem = this.text
                    root.checked(this.index, this.text)
                })
            }
        }
    }

    Component.onCompleted: {
        this.currentIndex = this.index
        this.currentItem = this.options[this.index]
    }
}
