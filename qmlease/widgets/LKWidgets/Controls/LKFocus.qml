import QtQuick 2.15

Item {
    id: root

    property bool   active: false
    property string scope: 'global'
    property var    __registeredFuncs: Object()
    property string __sid: py.qmlease.widget.generate_random_id()

    signal triggered(string fid)

    function register(key, modifier, func) {
        const sid = root.__sid
        const fid = py.qmlease.widget.generate_random_id()
        lkscope.register_func(
            root.scope, sid, fid, root, key, modifier
        )
        root.__registeredFuncs[fid] = func
    }

    Component.onCompleted: {
//        console.log(root.scope, root.__sid)
        lkscope.register_sid(root.scope, root.__sid)
        root.activeChanged.connect(() => {
            if (root.active) {
                lkscope.activate_scope(root.scope, root.__sid)
            } else {
                lkscope.deactivate_scope(root.scope, root.__sid)
            }
        })
        root.triggered.connect((fid) => {
            root.__registeredFuncs[fid]()
        })
        root.activeChanged()
    }
}
