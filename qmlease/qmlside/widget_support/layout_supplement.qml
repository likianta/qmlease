/*  some methods can only be used in qml runtime, such as anchor binding, -
 *  mouse event etc. since they don't proper converter for python to obtain, -
 *  we have to use them in qml context.
 *  this file is used by "./layout_engine.py" as supplemental methods provider.
 */
import QtQml 2.0

QtObject {
    function centerChild(parent, child, anchor) {
        switch (anchor) {
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
}
