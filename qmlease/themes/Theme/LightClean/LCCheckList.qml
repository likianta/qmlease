import QtQuick 2.15
import "./LCButtons"

LCListView {
    id: root

    property var p_checks: Object()  // {index: bool, ...}
    // inherits props:
    //      p_currentIndex
    //      p_delegate
    //      p_model
    //      p_scrollWidth
    //      p_spacing
    //      r_count
    //      r_currentItem

    signal clicked(int index, var checkbox)

    function getChecked() {  // -> [index, ...]
        let out = []
        for (var i in p_checks) {
            if (p_checks[i]) {
                out.push(i)
            }
        }
        return out
    }

    function getUnchecked() {  // -> [index, ...]
        let out = []
        for (var i in p_checks) {
            if (!p_checks[i]) {
                out.push(i)
            }
        }
        return out
    }

    function getCheckStates() {  // -> {index: bool, ...}
        return p_checks
    }

    function modifyDelegateItem(index, item, parent_) {
        // 如果您需要定制 delegateItem 的外观, 请在这里修改.
        // Examples:
        //      item.width = parent_.width / 2
    }

    function _get(obj, key, default_val) {
        /*  Inplement Python's `dict.get(key, default)` in Javascript.

            References:
                https://stackoverflow.com/questions/44184794/what-is-the
                -javascript-equivalent-of-pythons-get-method-for-dictionaries
         */
        const result = obj[key]
        if (typeof result !== 'undefined') {
            return result
        } else {
            return default_val
        }
    }

    p_delegate: LCCheckBox {
        width: root.r_preferredWidth
        p_text: modelData

        property int r_index: model.index

        onClicked: {
            root.p_checks[this.r_index] = this.checked
            root.clicked(this.r_index, this)
        }

        Component.onCompleted: {
            // console.log('[LCCheckList:73]', 'delegate item created',
            //             root.objectName, r_index)
            this.checked = _get(p_checks, model.index, false)
            modifyDelegateItem(this.r_index, this, root)
            /*  异常说明

                测试代码:
                    // view.qml
                    import LightClean 1.0

                    Item {
                        id: _item

                        function _modify(index, item, parent_) {
                            console.log(item.index, item.p_text)
                        }

                        LCCheckList {
                            p_model: ['A', 'B', 'C']

                            Component.onCompleted: {
                                // MARK_20201130_161629
                                this.delegateItemCreated.connect(
                                    _item._modify
                                )
                            }
                        }
                    }

                测试结果: 只有 '1, B', '2, C' 被打印了, '0, A' 却没有.

                初步怀疑是因为经历了以下流程:
                    1. LCCheckList 内部的 onCompleted 先被执行了 (也就是此时的信
                       号被发出去了, 但还没来得及建立 connection)
                    2. 然后 'MARK_20201130_161629' 这一步, 此时才建立 connection
                       但已经晚了, 所以 '0, A' 没有进入到 `_item._modify` 中
                    3. 这之后, connection 已经被建立, 所以之后赶来的 '1, B',
                       '2, C' 才得以进入 `_item._modify` (其实这里出现了两次重复
                       的 connect 动作, 是不好的)

                解决方法: 取消了 signal 方案, 改为 function 并由父组件覆写函数功
                能.
             */
            // delegateItemCreated(this.r_index, this, root)
            //      ↑ 不要使用 signal delegateItemCreated (此信号已从新版本中移
            //      除). 请通过覆写 function modifyDelegateItem 实现.
        }
    }
}
