import QtQuick
import LKWidgets

LKWindow {
    id: root
    title: 'LK Hot Reloader'
    width: 400
    height: 320

    LKRow {
        id: main_pane
        anchors.fill: parent
        anchors.margins: 8
        alignment: 'vcenter,stretch,vfill'
        spacing: 8

        Item {
            id: left_pane
            objectName: 'left_pane'

            LKRectangle2 {
                id: root_loader
                anchors {
                    left: parent.left
                    top: parent.top
                    right: parent.right
                    bottom: reload_button.top
                    bottomMargin: 4
                }

                Loader {
                    anchors.fill: parent
                    Component.onCompleted: {
                        pyloader.set_loader(this)
                    }
                }
            }

            LKButton {
                id: reload_button
                anchors {
                    left: parent.left
                    right: parent.right
                    bottom: parent.bottom
                }
                text: 'RELOAD'
                onClicked: pyloader.reload()
            }
        }

        Item {
            id: right_pane
            objectName: 'right_pane'

            LKText {
                anchors {
                    fill: parent
                    margins: 12
                }
                color: pycolor.theme_gray_3
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                text: 'the related watching files will be shown here.'
            }
        }
    }
}
