import QtQuick
import LKWidgets

LKWindow {
    id: root

    Item {
        id: _canvas
        anchors {
            fill: parent
            margins: 24
        }

        ListView {
            id: _listview
            anchors {
                fill: parent
            }
            model: py.main.qget('model')
            spacing: 8
            delegate: CellRect {
                color: model.color
                index: model.index
                label: model.label
                selected: index == _listview.currentIndex
                onForceFocused: (index) => {
                    _listview.currentIndex = index
                }
            }
        }

        LKText {
            visible: _listview.count == 0
            anchors.centerIn: parent
            text: 'Click the bottom button to add a new item'
        }
    }

    Toolbar {
        anchors {
            left: parent.left
            right: parent.right
            bottom: parent.bottom
            margins: 24
            bottomMargin: 8
        }
        listview: _listview
        model: _listview.model
    }
}
