import QtQuick 2.15
import "./LCButtons"

LCListView {
    id: root

    property int p_default: -1
    // extend props:
    //      p_currentIndex
    //      p_delegate
    //      p_model
    //      p_scrollWidth
    //      p_spacing
    //      r_count
    //      r_currentItem

    signal clicked(int index, var item)

    function modifyDelegateItem(index, item, parent_) {
        // See `LCCheckList.modifyDelegateItem`
    }

    p_delegate: LCRadioButton {
        id: _item
        width: root.r_preferredWidth
        p_text: modelData

        property int r_index: model.index

        onClicked: {
            root.currentIndex = r_index
            root.clicked(r_index, _item)
        }

        Component.onCompleted: {
            _item.checked = (p_default == r_index)
            modifyDelegateItem(this.r_index, this, root)
        }
    }

    Component.onCompleted: {
        if (p_default > -1) {
            root.currentIndex = p_default
        }
    }
}
