import QtQuick
import LKWidgets

LKWindow {

    LKColumn {
        anchors.centerIn: parent

        LKRow {
            LKRadioBox {
                ghostBorder: true
                text: 'AAA'
            }
            LKRadioBox {
                ghostBorder: true
                text: 'BBB'
            }
            LKRadioBox {
                ghostBorder: true
                text: 'CCC'
            }
        }

        LKRow {
            LKRadioBox {
                text: '111'
            }
            LKRadioBox {
                text: '222'
            }
            LKRadioBox {
                text: '333'
            }
        }
    }
}
