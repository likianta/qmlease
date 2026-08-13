/// Note: This file is a copy-paste from Row.qml, but with Column instead of 
/// Row.

import QtQuick as Q
import QmlEase as E

Q.Item {
    id: root
    clip: true
    implicitWidth: column.implicitWidth + borderWidth * 2
    implicitHeight: column.implicitHeight + borderWidth * 2

    default property alias content: column.data

    property bool   border: false // shorthand for borderWidth
    property bool   borderColor: pycolor.outline
    property int    borderWidth: border ? 1 : 0
    property string color: pycolor.transparent
    property string halign: 'none' // 'none', 'stretch', 'center'
    property int    spacing: 4
    property string valign: 'none' // 'none', 'stretch'

    function computeLayout() {
        // layout system: 
        // https://chatgpt.com/share/6a7d8213-fe00-83e8-95e5-2e88a0dceb92
        if (root.width <= 0 || root.height <= 0) {
            return
        }

        const children = column.children

        // vertical dimension
        if (root.valign == "stretch") {
            let stretchChildren = []
            let fixedHeight = 0
            let totalStretch = 0

            for (let child of children) {
                // console.log(
                //     child._stretch, 
                //     child._stretch === undefined, 
                //     child._stretch > 0
                // )
                if (child._stretch === undefined) {
                    fixedHeight += child.height > 0 ? 
                        child.height : child.implicitHeight
                } else {
                    const stretch = child._stretch
                    stretchChildren.push(child)
                    totalStretch += stretch
                }
            }

            if (stretchChildren.length > 0 && totalStretch > 0) {
                const totalSpacing = children.length > 1 ? 
                    column.spacing * (children.length - 1) : 0
                const availableHeight = 
                    column.height - 
                    column.topPadding - column.bottomPadding - totalSpacing
                const unallocatedHeight = availableHeight - fixedHeight
                // console.log(
                //     root.height, 
                //     availableHeight, 
                //     fixedHeight, 
                //     unallocatedHeight, 
                //     totalStretch
                // )
                if (unallocatedHeight > 0) {
                    const unitHeight = unallocatedHeight / totalStretch
                    for (let child of stretchChildren) {
                        child.height = unitHeight * child._stretch
                    }
                }
            }
        }

        // horizontal dimension
        if (root.halign == 'stretch') {
            const resonableWidth = 
                column.width - column.topPadding - column.bottomPadding
            for (let child of children) {
                child.width = resonableWidth
            }
        } else if (root.halign == 'center') {
            for (let child of children) {
                child.anchors.horizontalCenter = 
                    Qt.binding(() => column.horizontalCenter)
            }
        }
    }

    E.Rectangle {
        anchors.fill: parent
        border.width: root.borderWidth
        border.color: root.borderColor
        color: root.color

        Q.Column {
            id: column
            anchors {
                fill: parent
                margins: root.borderWidth
            }
            spacing: root.spacing
            // Q.Component.onCompleted: {
            //     root.computeLayout()
            // }
        }
    }

    Q.Component.onCompleted: {
        // pylayout.inspect_size(this, 'column layout')
        // pylayout.inspect_size(column, 'inner column layout')
        root.widthChanged.connect(root.computeLayout)
        root.heightChanged.connect(root.computeLayout)
        root.halignChanged.connect(root.computeLayout)
        root.valignChanged.connect(root.computeLayout)
        if (root.halign != 'none' || root.valign != 'none') {
            root.computeLayout()
        }
    }
}
