import QtQuick
import LKWidgets

Row {
    id: root
    spacing: 12
    height: childrenRect.height
    
    property var listview
    property var model

    LKButton {
        text: 'Add item'
        onClicked: {
            root.model.append({})
        }
    }

    LKButton {
        text: 'Insert item'
        onClicked: {
            root.model.insert(root.listview.currentIndex + 1, {})
            root.listview.currentIndex += 1
            root.listview.currentItem.activate()
        }
    }

    LKButton {
        text: 'Delete item'
        onClicked: {
            let nextItem
            if (root.listview.currentIndex == root.listview.count - 1) {
                nextItem = root.listview.itemAtIndex(
                    root.listview.currentIndex - 1
                )
            } else {
                nextItem = root.listview.itemAtIndex(
                    root.listview.currentIndex + 1
                )
            }
            root.model.delete(root.listview.currentIndex)
            nextItem.activate()
        }
    }

    LKButton {
        text: 'Move up'
        onClicked: {
            if (root.listview.currentIndex > 0) {
                root.model.move_up(root.listview.currentIndex)
                root.listview.currentIndex -= 1
                root.listview.currentItem.activate()
            }
        }
    }
    
    LKButton {
        text: 'Move down'
        onClicked: {
            if (root.listview.currentIndex < root.listview.count - 1) {
                root.model.move_down(root.listview.currentIndex)
                root.listview.currentIndex += 1
                root.listview.currentItem.activate()
            }
        }
    }

    LKButton {
        text: 'Reset'
        onClicked: {
            py.main.reset()
        }
    }
}
