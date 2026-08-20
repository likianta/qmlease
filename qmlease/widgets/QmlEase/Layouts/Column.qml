// This file was auto translated from ./Row.qml, please do not 
// modify it manuall.
// Translator: sidework/translate_row_to_column.py

import QtQuick
import QtQuick as Q
import "../Visual" as V

Item {
    id: root
    // note: if you want to animate the background width or height, do not use 
    // `Behavior on width` directly; use `Behavior on implicitWidth` instead.
    // property alias  backgroundWidth: root.width
    // property alias  backgroundHeight: root.height
    implicitWidth: 
        finalLeftMargin + 
        borderWidth +
        column.implicitWidth + 
        borderWidth +
        finalRightMargin
    implicitHeight: 
        finalTopMargin + 
        borderWidth +
        column.implicitHeight + 
        borderWidth +
        finalBottomMargin
    clip: true

    default property alias content: column.data

    property int    bmargin: -1
    property bool   border: false // shorthand for borderWidth
    property string borderColor: pycolor.outline
    property int    borderRadius: 8
    property int    borderWidth: border ? 1 : 0
    property int    bpadding: -1
    property string color: pycolor.transparent
    property int    finalBottomMargin:
        bmargin >= 0 ? bmargin :
        vmargin >= 0 ? vmargin :
        margin >= 0 ? margin :
        0
    property int    finalBottomPadding: 
        bpadding >= 0 ? bpadding :
        vpadding >= 0 ? vpadding :
        padding >= 0 ? padding :
        0
    property int    finalLeftMargin:
        lmargin >= 0 ? lmargin :
        hmargin >= 0 ? hmargin :
        margin >= 0 ? margin :
        0
    property int    finalLeftPadding: 
        lpadding >= 0 ? lpadding :
        hpadding >= 0 ? hpadding :
        padding >= 0 ? padding :
        0
    property int    finalRightMargin:
        rmargin >= 0 ? rmargin :
        hmargin >= 0 ? hmargin :
        margin >= 0 ? margin :
        0
    property int    finalRightPadding: 
        rpadding >= 0 ? rpadding :
        hpadding >= 0 ? hpadding :
        padding >= 0 ? padding :
        0
    property int    finalTopMargin:
        tmargin >= 0 ? tmargin :
        vmargin >= 0 ? vmargin :
        margin >= 0 ? margin :
        0
    property int    finalTopPadding: 
        tpadding >= 0 ? tpadding :
        vpadding >= 0 ? vpadding :
        padding >= 0 ? padding :
        0
    property string halign: 'start' // start, stretch, center
    property int    hmargin: -1
    property int    hpadding: -1
    property int    lmargin: -1
    property int    lpadding: -1
    property int    margin: -1
    property int    padding: -1
    property int    rmargin: -1
    property int    rpadding: -1
    property int    tmargin: -1
    property int    tpadding: -1
    property int    spacing: 8
    property string valign: 'start' // start, stretch
    property int    vmargin: -1
    property int    vpadding: -1

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
                column.width - column.leftPadding - column.rightPadding
            for (let child of children) {
                child.width = resonableWidth
            }
        } else if (root.halign == 'center') {
            // for (let child of children) {
            //     child.anchors.horizontalCenter = 
            //         Qt.binding(() => column.horizontalCenter)
            // }
            
            const resonableWidth = 
                column.width - column.leftPadding - column.rightPadding
            let childWidth = 0
            for (let child of children) {
                childWidth = child.width > 0 ? 
                    child.width : child.implicitWidth
                child.x = (column.width - childWidth) / 2
            }
        }
    }

    V.Rectangle {
        id: background
        anchors {
            fill: parent
            leftMargin: root.finalLeftMargin
            topMargin: root.finalTopMargin
            rightMargin: root.finalRightMargin
            bottomMargin: root.finalBottomMargin
        }
        border.width: root.borderWidth
        border.color: root.borderColor
        // clip: true
        color: root.color
        radius: root.borderRadius

        Q.Column {
            id: column
            anchors {
                fill: parent
                margins: root.borderWidth
            }
            bottomPadding: root.finalBottomPadding
            leftPadding: root.finalLeftPadding
            rightPadding: root.finalRightPadding
            topPadding: root.finalTopPadding
            spacing: root.spacing
            // Component.onCompleted: {
            //     root.computeLayout()
            // }
        }
    }

    Component.onCompleted: {
        // pylayout.inspect_size(this, 'column layout')
        // pylayout.inspect_size(column, 'inner column layout')
        root.widthChanged.connect(root.computeLayout)
        root.heightChanged.connect(root.computeLayout)
        root.halignChanged.connect(root.computeLayout)
        root.valignChanged.connect(root.computeLayout)
        if (root.halign != 'start' || root.valign != 'start') {
            root.computeLayout()
        }
    }
}
