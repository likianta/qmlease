import QtQuick
import QtQuick.Layouts
import QmlEase
import QmlEase.Layouts

Window {
    id: root

    property real  ratio: 0.5
    // property string rectColor0: '#0969da'
    // property string rectColor1: '#ecefff'
    property alias rectColor0: color0Input.text
    property alias rectColor1: color1Input.text

    signal colorPairChanged(string color0, string color1)
    // signal requestContainerColorLight(string color)
    // signal requestContainerColorDark(string color)

    Vertical {
        anchors {
            centerIn: parent
        }
        width: 400

        TextInput {
            id: color0Input
            Layout.fillWidth: true
            label: 'Container color'
            text: '#0969da'
        }

        TextInput {
            id: color1Input
            Layout.fillWidth: true
            label: 'OnContainer color'
            text: '#ecefff'
        }

        // TabsLayout {
        //     model: ['Preview', 'Container']
        // }

        // preview
        Vertical {
            // Layout.alignment: Qt.AlignHCenter
            Layout.fillWidth: true

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 240
                border.width: 2
                border.color: pycolor.outline_variant
                color: pycolor.transparent

                Rectangle {
                    anchors {
                        centerIn: parent
                    }
                    width: 200
                    height: 200
                    color: root.rectColor0

                    Rectangle {
                        anchors {
                            centerIn: parent
                        }
                        width: 100
                        height: 100
                        color: root.rectColor1
                    }
                }
            }

            Text {
                Layout.alignment: Qt.AlignHCenter
                text: `Ratio: ${root.ratio}`
            }
        }

        Horizontal {
            Layout.fillWidth: true
            Button {
                text: 'Swap'
                onClicked: {
                    const temp = root.rectColor0
                    root.rectColor0 = root.rectColor1
                    root.rectColor1 = temp
                    root.colorPairChanged(root.rectColor0, root.rectColor1)
                }
            }
            Button {
                text: 'Make container light'
                onClicked: {
                    // root.requestContainerColorLight(root.rectColor1)
                    py.main.make_container_color(root.rectColor1, true)
                }
            }
            Button {
                text: 'Make container dark'
                onClicked: {
                    // root.requestContainerColorDark(root.rectColor1)
                    py.main.make_container_color(root.rectColor1, false)
                }
            }
        }
    }

    Component.onCompleted: {
        color0Input.editingFinished.connect((text) => {
            // root.rectColor0 = text
            root.colorPairChanged(text, root.rectColor1)
        })
        color1Input.editingFinished.connect((text) => {
            // root.rectColor1 = text
            root.colorPairChanged(root.rectColor0, text)
        })
        py.main.init_ui(root)
    }
}