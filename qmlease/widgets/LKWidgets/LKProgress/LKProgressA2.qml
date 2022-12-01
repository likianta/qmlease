import QtQuick 2.15

ProgBase2 {
    id: root

    property int  precision: 0  // suggested 0 or 2
    property real __value

    delegate: LKProgressA {
        Component.onCompleted: {
            root.__value = Qt.binding(() => this.__progValue)
        }
    }

    Behavior on __value {
        NumberAnimation {
            duration: root.demoMode ? 500 : 100
        }
    }

    Component.onCompleted: {
        this.textItem.maxText = Qt.binding(
            () => lkprogress.show_value(1.0, root.precision)
        )
        this.textItem.text = Qt.binding(
            () => lkprogress.show_value(
                root.__value, root.precision
            )
        )
    }
}
