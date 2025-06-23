import QtQuick 2.15
import ".." as A
import "../Layouts" as B

B.LKRow {
    id: root
    alignment: 'vfill'
    autoSize: true

    property alias text: _input.text
    property alias title: _title.text
    property alias titleWidth: _title.width

    A.LKText {
        id: _title
    }

    LKInput {
        id: _input
        width: pysize.stretch
    }

//    Component.onCompleted: {
//        this.titleWidthChanged.connect(() => root.resize())
//    }
}
