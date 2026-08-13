import QtQuick as Q
import QmlEase as E

Q.Item {
    id: root
    clip: true
    implicitWidth: row.implicitWidth + borderWidth * 2
    implicitHeight: row.implicitHeight + borderWidth * 2

    default property alias content: row.data

    property bool   border: false // shorthand for borderWidth
    property bool   borderColor: pycolor.outline
    property int    borderWidth: border ? 1 : 0
    property string color: pycolor.transparent
    property string halign: 'none' // 'none', 'stretch'
    property int    spacing: 4
    property string valign: 'none' // 'none', 'stretch', 'center'

    function computeLayout() {
        // layout system: 
        // https://chatgpt.com/share/6a7d8213-fe00-83e8-95e5-2e88a0dceb92
        if (root.width <= 0 || root.height <= 0) {
            return
        }

        const children = row.children

        // horizontal dimension
        if (root.halign == "stretch") {
            let stretchChildren = []
            let fixedWidth = 0
            let totalStretch = 0

            for (let child of children) {
                // console.log(
                //     child._stretch, 
                //     child._stretch === undefined, 
                //     child._stretch > 0
                // )
                if (child._stretch === undefined) {
                    fixedWidth += child.width > 0 ? 
                        child.width : child.implicitWidth
                } else {
                    const stretch = child._stretch
                    stretchChildren.push(child)
                    totalStretch += stretch
                }
            }

            if (stretchChildren.length > 0 && totalStretch > 0) {
                const totalSpacing = children.length > 1 ? 
                    row.spacing * (children.length - 1) : 0
                const availableWidth = 
                    row.width - 
                    row.leftPadding - row.rightPadding - totalSpacing
                const unallocatedWidth = availableWidth - fixedWidth
                // console.log(
                //     root.width, 
                //     availableWidth, 
                //     fixedWidth, 
                //     unallocatedWidth, 
                //     totalStretch
                // )
                if (unallocatedWidth > 0) {
                    const unitWidth = unallocatedWidth / totalStretch
                    for (let child of stretchChildren) {
                        child.width = unitWidth * child._stretch
                    }
                }
            }
        }

        // vertical dimension
        if (root.valign == 'stretch') {
            const resonableHeight = 
                row.height - row.topPadding - row.bottomPadding
            for (let child of children) {
                child.height = resonableHeight
            }
        } else if (root.valign == 'center') {
            for (let child of children) {
                child.anchors.verticalCenter = 
                    Qt.binding(() => row.verticalCenter)
            }
        }
    }

    E.Rectangle {
        anchors.fill: parent
        border.width: root.borderWidth
        border.color: root.borderColor
        color: root.color

        Q.Row {
            id: row
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
        // pylayout.inspect_size(this, 'row layout')
        // pylayout.inspect_size(row, 'inner row layout')
        root.widthChanged.connect(root.computeLayout)
        root.heightChanged.connect(root.computeLayout)
        root.halignChanged.connect(root.computeLayout)
        root.valignChanged.connect(root.computeLayout)
        if (root.halign != 'none' || root.valign != 'none') {
            root.computeLayout()
        }
    }
}
