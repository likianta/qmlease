import QtQuick

Item {
    id: root
    width: rm_shape.width_100p
    height: rm_shape.height

    // properties
    // spacing

    Component.onCompleted: {
        pyside.eval(`
            from lk_qtquick_scaffold import eval_js

            spared_width = {}  # dict[int child_index, float width]

            def get_children(parent):
                return eval_js('''
                    return {parent}.children
                ''', {'parent': parent})

            def bind_anchors(item_a, anchor_a, item_b, anchor_b):
                eval_js('''
                    {item_a}.anchors.{anchor_a} = Qt.binding(() => {
                        return {item_b}.{anchor_b}
                    }))
                ''', {'item_a': item_a, 'anchor_a': anchor_a,
                      'item_b': item_b, 'anchor_b': anchor_b})

            children = get_children(parent)
            curr_index = -1
            for last_item, curr_item, next_item in zip(
                (parent, *children[:-1]),
                (children),
                (*children[1:], parent),
            ):
                curr_index += 1

                if curr_index == 0:



            for i, item in enumerate(get_children(parent))):
                if i == 0:
                    bind_anchors(item, 'left', parent, 'left')



        `, {'parent': root})


        let i, child
        let width_undefined_children = new Array()

        for (i in root.children) {
            child = root.children[i]

            // finalize width
            if (child.width == 0) {
                width_undefined_children.push()
            }


            // finalize height
            if (child.height == 0) {
                // child.height = Qt.binding(() => root.height)
                child.height = root.height
            } else if (child.height < 1) {
                const ratio = child.height
                child.height = root.height * ratio
            }
        }
    }
}
