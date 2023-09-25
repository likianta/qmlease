import QtQuick

Item {
    id: root
    clip: true

    property int  howSize   : pyenum.WRAP
    property int  howSpacing: pyenum.AUTO
//    property int  margin: 0
    property int  hmargin : 0
    property int  vmargin : 0
    property int  tmargin : 0
    property int  rmargin : 0
    property int  bmargin : 0
    property int  lmargin : 0
    property int  padding : 0
    property int  hpadding: 0
    property int  vpadding: 0
    property int  tpadding: 0
    property int  rpadding: 0
    property int  bpadding: 0
    property int  lpadding: 0
    property int  spacing : 0
    property int  hspacing: 0
    property int  vspacing: 0
    property int  tspacing: 0
    property int  rspacing: 0
    property int  bspacing: 0
    property int  lspacing: 0
    property bool _lock: false

    Component.onCompleted: {
        root.marginChanged.connect(() => {
            root._lock = true
            root.hmargin = root.margin
            root.vmargin = root.margin
            root.tmargin = root.margin
            root.rmargin = root.margin
            root.bmargin = root.margin
            root.lmargin = root.margin
            root._lock = false
        })
        root.hmarginChanged.connect(() => {
            if (root._lock) return
            root.lmargin = root.hmargin
            root.rmargin = root.hmargin
        })
        root.vmarginChanged.connect(() => {
            if (root._lock) return
            root.tmargin = root.vmargin
            root.bmargin = root.vmargin
        })

        root.paddingChanged.connect(() => {
            root._lock = true
            root.hpadding = root.padding
            root.vpadding = root.padding
            root.tpadding = root.padding
            root.rpadding = root.padding
            root.bpadding = root.padding
            root.lpadding = root.padding
            root._lock = false
        })
        root.hpaddingChanged.connect(() => {
            if (root._lock) return
            root.lpadding = root.hpadding
            root.rpadding = root.hpadding
        })
        root.vpaddingChanged.connect(() => {
            if (root._lock) return
            root.tpadding = root.vpadding
            root.bpadding = root.vpadding
        })

        root.spacingChanged.connect(() => {
            root.hspacing = root.spacing
            root.vspacing = root.spacing
        })
    }
}
