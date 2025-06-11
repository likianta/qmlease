import QtQuick 2.15
import ".." as A
import "../Buttons" as B

Flow {
    id: root
    width: pyenum.auto
    height: pyenum.auto
    flow: horizontal ? Flow.LeftToRight : Flow.TopToBottom
    spacing: pysize.spacing_m

    property bool  ghostBorder: true
    property bool  horizontal: false
    property int   index: 0
    property alias model: _repeater.model
    property alias title: _text.text

    signal checked(int index, string label)

    A.LKText {
        id: _text
        height: pysize.item_height
        horizontalAlignment: Text.AlignLeft
        verticalAlignment: Text.AlignVCenter
    }

    Repeater {
        id: _repeater
        width: root.horizontal ? pysize.item_width : root.width
        height: root.horizontal ? root.height : pysize.item_height

        delegate: B.LKRadioBox {
            // width: root.horizontal ? childrenRect.width : root.width
            // height: root.height
            ghostBorder: root.ghostBorder
            text: modelData

            property int index: model.index

            Component.onCompleted: {
                if (!root.horizontal) {
                    this.width = root.width
                }
                if (this.index == root.index) {
                    this.checked = true
                }
                this.onToggled.connect(() => {
                    root.index = this.index
                    root.checked(this.index, this.text)
                })
            }
        }
    }

    Component.onCompleted: {
        py.qmlease.widget.init_radio_group(this)
    }
}
