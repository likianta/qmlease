/*  some methods can only be used in qml runtime, such as anchor binding, -
 *  mouse event etc. since they don't proper converter for python to obtain, -
 *  we have to use them in qml context.
 *  this file is used by "./layout_engine.py" as supplemental methods provider.
 */
import QtQml 2.0

QtObject {
    function alignChild(parent, child, anchor) {
        switch (anchor) {
            case 'center':
                child.anchors.centerIn = Qt.binding(
                    () => parent
                )
                break
            case 'hcenter':
                child.anchors.horizontalCenter = Qt.binding(
                    () => parent.horizontalCenter
                )
                break
            case 'vcenter':
                child.anchors.verticalCenter = Qt.binding(
                    () => parent.verticalCenter
                )
                break
            case 'left':
                child.anchors.left = Qt.binding(() => parent.left)
                break
            case 'top':
                child.anchors.top = Qt.binding(() => parent.top)
                break
            case 'right':
                child.anchors.right = Qt.binding(() => parent.right)
                break
            case 'bottom':
                child.anchors.bottom = Qt.binding(() => parent.bottom)
                break
        }
    }

    function inferSize(item, dimension) {
        if (dimension == 'horizontal') {
            item.width = Qt.binding(() => item.implicitWidth)
        } else {
            item.height = Qt.binding(() => item.implicitHeight)
        }
    }

    function marginChild(parent, child, margins) {
        if (margins[0] > 0) {
            child.anchors.top = Qt.binding(() => parent.top)
            child.anchors.topMargin = margins[0]
        }
        if (margins[1] > 0) {
            child.anchors.right = Qt.binding(() => parent.right)
            child.anchors.rightMargin = margins[1]
        }
        if (margins[2] > 0) {
            child.anchors.bottom = Qt.binding(() => parent.bottom)
            child.anchors.bottomMargin = margins[2]
        }
        if (margins[3] > 0) {
            child.anchors.left = Qt.binding(() => parent.left)
            child.anchors.leftMargin = margins[3]
        }
    }

    function wrapSize(item, dimension, shift=0) {
        if (dimension == 'horizontal') {
            item.width = Qt.binding(() => item.childrenRect.width + shift)
        } else {
            item.height = Qt.binding(() => item.childrenRect.height + shift)
        }
    }

    function wrapSize2(target, ref, hshift, vshift) {
        target.width = Qt.binding(() => ref.width + hshift)
        target.height = Qt.binding(() => ref.height + vshift)
    }
}
