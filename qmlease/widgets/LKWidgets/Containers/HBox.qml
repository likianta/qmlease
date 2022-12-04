import QtQuick

Box {
    id: root

    property int alignment: pyenum.LEFT
    property int howSize: pyenum.WRAP
    property int howSpacing: pyenum.NONE
    property int padding: 0
    property int lpadding: 0
    property int rpadding: 0
    property int spacing: 0

    Row {
        id: row
        spacing: root.spacing
        Component.onCompleted: {
            pylayout.auto_size_children(this, 'h')
            root.howSpacingChanged.connect(() => {
                pylayout.auto_spacing(this, root.howSpacing, 'h')
            })
            root.lpaddingChanged.connect(() => {
                pylayout.auto_spacing(this, root.howSpacing, 'h')
            })
            root.rpaddingChanged.connect(() => {
                pylayout.auto_spacing(this, root.howSpacing, 'h')
            })
        }
    }

    Binding {
        id: justify_left
        target: row
        when: _isBindingEnabled(pyenum.LEFT)
        property: 'anchors.left'
        value: root.left
    }

    Binding {
        id: justify_center
        target: row
        when: _isBindingEnabled(pyenum.CENTER)
        property: 'anchors.horizontalCenter'
        value: root.horizontalCenter
    }

    Binding {
        id: justify_right
        target: row
        when: _isBindingEnabled(pyenum.RIGHT)
        property: 'anchors.right'
        value: root.right
    }

    function _isBindingEnabled(expect) {
        if (root.howSize == pyenum.FILL) {
            return expect == root.justify
        } else {
            return false
        }
    }

    Component.onCompleted: {
        root.paddingChanged.connect(() => {
            root.lpadding = root.padding
            root.rpadding = root.padding
        })
    }
}
