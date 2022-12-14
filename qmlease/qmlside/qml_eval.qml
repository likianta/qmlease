import QtQml 2.0

QtObject {
    function bindAnchorsToParent(child, parent, anchors_, margins_) {
        /*
         *  args:
         *      anchors_:
         *          one word: 'centerIn', 'fill'
         *          one or many words, joined by any separator:
         *              'top', 'right', 'bottom', 'left',
         *              'horizontalCenter', 'verticalCenter'
         *          the separator is suggested to be space, comma or semicolon.
         *          if given `null`, no anchor will be set.
         *      margins_:
         *          union[int, tuple[int, int], tuple[int, int, int, int]]
         *              int: all margins are set to the same value.
         *              tuple[int, int]: top and bottom margins are set to the
         *                  first value, left and right margins are set to the
         *                  second value.
         *              tuple[int, int, int, int]: top, right, bottom and left
         *                  margins are respectively set.
         *          if given `null`, no margin will be set.
         */
        if (anchors_) {
            if (anchors_ == 'centerIn') {
                child.anchors.centerIn = Qt.binding(() => parent)
            } else if (anchors_ == 'fill') {
                child.anchors.fill = Qt.binding(() => parent)
            } else {
                if (anchors_.includes('top')) {
                    child.anchors.top = Qt.binding(() => parent.top)
                }
                if (anchors_.includes('bottom')) {
                    child.anchors.bottom = Qt.binding(() => parent.bottom)
                }
                if (anchors_.includes('left')) {
                    child.anchors.left = Qt.binding(() => parent.left)
                }
                if (anchors_.includes('right')) {
                    child.anchors.right = Qt.binding(() => parent.right)
                }
                if (anchors_.includes('hcenter') ||
                    anchors_.includes('horizontalCenter')) {
                    child.anchors.horizontalCenter = Qt.binding(
                        () => parent.horizontalCenter
                    )
                }
                if (anchors_.includes('vcenter') ||
                    anchors_.includes('verticalCenter')) {
                    child.anchors.verticalCenter = Qt.binding(
                        () => parent.verticalCenter
                    )
                }
            }
        }

        if (margins_ !== null) {
            if (margins_.length == 1) {
                child.anchors.margins = margins_[0]
            } else if (margins_.length == 2) {
                child.anchors.topMargin = margins_[0]
                child.anchors.bottomMargin = margins_[0]
                child.anchors.leftMargin = margins_[1]
                child.anchors.rightMargin = margins_[1]
            } else if (margins_.length == 4) {
                child.anchors.topMargin = margins_[0]
                child.anchors.rightMargin = margins_[1]
                child.anchors.bottomMargin = margins_[2]
                child.anchors.leftMargin = margins_[3]
            }
        }
    }

    function bindAnchorsToSibling(one, another, anchors_, margins_) {
        /*
         *  args:
         *      anchors_:
         *          optional[list[tuple[str one_side, str another_side]]]
         *              the side is one of 'top', 'right', 'bottom', 'left',
         *              'horizontalCenter', 'verticalCenter'.
         *      margins_: the same as `bindAnchorsToParent`.
         */
        if (anchors_) {
            for (let i = 0; i < anchors_.length; i++) {
                let one_side = anchors_[i][0]
                let another_side = anchors_[i][1]
                eval(`one.anchors.${one_side}`) = Qt.binding(
                    () => eval(`another.${another_side}`)
                )
            }
        }

        if (margins_ !== null) {
            if (margins_.length == 1) {
                one.anchors.margins = margins_[0]
            } else if (margins_.length == 2) {
                one.anchors.topMargin = margins_[0]
                one.anchors.bottomMargin = margins_[0]
                one.anchors.leftMargin = margins_[1]
                one.anchors.rightMargin = margins_[1]
            } else if (margins_.length == 4) {
                one.anchors.topMargin = margins_[0]
                one.anchors.rightMargin = margins_[1]
                one.anchors.bottomMargin = margins_[2]
                one.anchors.leftMargin = margins_[3]
            }
        }
    }

    function bindProp(a, b, prop) {
        eval(`a.${prop}`) = Qt.binding(() => eval(`b.${prop}`))
    }
}

