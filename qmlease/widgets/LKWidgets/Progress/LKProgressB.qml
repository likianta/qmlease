import QtQuick 2.15

ProgBase {
    id: root

    property var model
    //  dict[float|str key, str value]
    //      key: the value range from 0.0 to 1.0.
    //      MUST: at least two keys in the dict. one for min value (0.0) and
    //          one for max (1.0).
    property var __model
    //  dict[float rounded_key, str value]
    //      rounded_key: the precision is 0.00001 (5 digits).

    signal stepChanged(int step)

    progFgDelegate: ProgFgB {
        id: _fg

        property real value
//        property var  __valueToStep

        Component.onCompleted: {
            this.stepChanged.connect(() => root.stepChanged(this.step))

            root.__modelChanged.connect(() => {
                this.totalSteps = pyside.eval(`
                    return len(model)
                `, {'model': root.__model})

//                this.__valueToStep = pyside.eval(`
//                    return {k: i for i, k in enumerate(model)}
//                `, {'model': root.__model})
            })

            this.valueChanged.connect(() => {
                this.step = pyside.eval(`
                    return min(
                        enumerate(model),
                        key=lambda x: abs(x[1] - value)
                    )[0]
                `, {
                    'model': root.__model,
                    'value': this.value
                })
            })

            this.clicked.connect((step) => {
                root.progValue = pyside.eval(`
                    return tuple(model)[index]
                `, {'model': root.__model, 'index': step})
            })
        }
    }

    Item {
        id: _invisible_draggee
    }

    MouseArea {
        visible: root.demoMode
        anchors.fill: parent
        drag.target: _invisible_draggee
        onClicked: (mouse) => {
            root.progValue = mouse.x / root.progWidth
        }
        onPositionChanged: (mouse) => {
            if (this.drag.active) {
                root.progValue = mouse.x / root.progWidth
            }
        }
    }

    Component.onCompleted: {
        this.progBgItem.width = Qt.binding(() => {
            return this.width - pysize.dot_radius_active * 2
        })
        this.modelChanged.connect(() => {
            if (this.model) {
                this.__model = pyside.eval(`
                    try:
                        return {round(float(k), 5): v
                                for k, v in model.items()}
                    except:
                        return {}
                `, {'model': this.model})
            } else {
                this.__model = {}
            }
        })
        this.progValueChanged.connect(() => {
            this.__progValue = lkprogress.get_nearest_progress(
                this.progValue, this.__model
            )
        })
        this.modelChanged()
    }
}
