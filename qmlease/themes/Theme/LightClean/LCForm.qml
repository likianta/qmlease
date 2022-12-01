import QtQuick 2.15

Item {
    /*
        Usages:
            // view.qml
            import LightClean 1.0
            LCForm {
                LCText {
                    property string p_key: 'My Text 1'
                    property alias  p_val: text
                }
                LCText {
                    property string p_key: 'My Text 2'
                    property alias  p_val: text
                }
                Component.onCompleted: {
                    this.post('Resolve text in Python backend')
                }
            }
     */
    property var p_data: Object()

    function collectData(rootItem) {
        let i, child
        for (i in rootItem.children) {
            child = rootItem.children[i]
            if (child.p_key) {
                p_data[child.p_key] = child.p_val
            } else {
                collectData(child)  // function will finally return global variant `p_data`, but no need to receive 
                //      it in recursive loops since it is global variant.
            }
        }
        return p_data
    }

    function post(name) {
        return PyHandler.main(name, collectData(this))
    }
}