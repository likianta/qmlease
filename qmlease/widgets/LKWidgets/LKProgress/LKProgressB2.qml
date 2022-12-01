import QtQuick 2.15

ProgBase2 {
    id: root
    width: pysize.bar_width
    height: pysize.bar_height

    property var  model
    property var  __model
    property real __value

    signal stepChanged(int step)

    delegate: LKProgressB {
        model: root.model
        Component.onCompleted: {
            this.stepChanged.connect(root.stepChanged)
            root.__model = Qt.binding(() => this.__model)
            root.__value = Qt.binding(() => this.__progValue)
        }
    }

    Component.onCompleted: {
        this.__valueChanged.connect(() => {
            if (this.__model) {
                this.textItem.text = lkprogress.get_nearest_value(
                    this.__value, this.__model
                )
            }
        })
        this.__modelChanged.connect(() => {
            if (this.__model) {
                this.textItem.maxText = pyside.eval(`
                    return max(map(str, model.values()), key=len)
                `, {'model': this.__model})
            }
            this.__valueChanged()
        })
    }
}
