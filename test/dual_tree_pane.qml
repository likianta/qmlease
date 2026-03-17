import QtQuick
import QtQuick.Layouts
import QmlEase
import QmlEase.Composites

Window {
    RowLayout {
        anchors {
            fill: parent
            margins: 24
        }
        spacing: 12

        TreeView {
            id: _leftTree
            Layout.fillWidth: true
            Layout.fillHeight: true
            // Layout.preferredHeight: 500
            checkable: true
            expandRoot: true
        }

        TreeView {
            id: _rightTree
            Layout.fillWidth: true
            Layout.fillHeight: true
            // Layout.preferredHeight: 500
            checkable: false
            expandRoot: true
        }
    }

    Component.onCompleted: {
        console.log(
            _leftTree.x,
            _leftTree.y,
            _leftTree.width,
            _leftTree.height,
        )
        py.main.init_ui(_leftTree, _rightTree)
    }
}
