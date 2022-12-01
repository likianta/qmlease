import QtQuick 2.15

ProgBase {
    id: root

    progFgDelegate: ProgFgA {
        Behavior on value {
            enabled: root.demoMode
            NumberAnimation {
                duration: 500
                easing.type: Easing.OutQuad
            }
        }
    }

    MouseArea {
        visible: root.demoMode
        anchors.fill: parent
        property bool __switch: false
        onClicked: {
            this.__switch = !this.__switch
            root.progValue = this.__switch ? 1 : 0
        }
    }

    Component.onCompleted: {
        this.progValueChanged.connect(() => {
            if (this.progValue <= 0) {
                this.__progValue = 0
            } else if (this.progValue >= 1) {
                this.__progValue = 1
            } else {
                this.__progValue = this.progValue
            }
        })
    }
}
