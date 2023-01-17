import QtQuick
import LKWidgets

LKWindow {

    LKColumn {
        anchors.centerIn: parent

        LKRow {
            LKRadioBox {
                showGhostBorder: true
                text: 'AAA'
            }
            LKRadioBox {
                showGhostBorder: true
                text: 'BBB'
            }
            LKRadioBox {
                showGhostBorder: true
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
