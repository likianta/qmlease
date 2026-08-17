import QtQuick
import QtQuick.Controls
import "../Controls" as C
import "../Layouts" as L
import "../Visual" as V

Item {
    id: root
    clip: false
    implicitWidth: _trigger.implicitWidth
    implicitHeight: _trigger.implicitHeight

    property int    currentIndex: 0
    property bool   expanded: _popup.opened
    property var    model: []
    property int    widthHint: 200

    signal selected(int index, string text)

    L.Row {
        id: _trigger
        implicitWidth: root.widthHint
        implicitHeight: 36
        borderWidth: 1
        borderColor: pycolor.outline
        color: (
            mouse.pressed ?
            pycolor.higher(pycolor.container, 1) :
            pycolor.container
        )
        lpadding: 12
        rpadding: 8
        valign: 'center'
        spacing: 8

        property string _currentLabel: (
            root.model[root.currentIndex] === undefined ?
            '' :
            typeof root.model[root.currentIndex] === 'string' ?
            root.model[root.currentIndex] :
            root.model[root.currentIndex].label
        )

        V.Text {
            width: root.widthHint - 40
            color: pycolor.on_container
            elide: Text.ElideRight
            text: _trigger._currentLabel
        }

        V.Icon {
            anchors.right: parent.right
            size: 16
            source: '../Resources/arrow-down-s-line.svg'
            color: pycolor.text_secondary
            rotation: root.expanded ? 180 : 0

            Behavior on rotation {
                NumberAnimation {
                    duration: 100
                }
            }
        }

        C.MouseArea {
            id: mouse
            anchors.fill: parent
            onClicked: {
                if (root.expanded) {
                    _popup.close()
                } else {
                    _popup.open()
                }
            }
        }
    }

    Popup {
        id: _popup
        x: 0
        y: _trigger.height + 4
        width: root.implicitWidth
        padding: 0
        closePolicy: Popup.CloseOnEscape |
                     Popup.CloseOnPressOutsideParent

        background: V.Rectangle {
            width: parent.width
            height: parent.height
            border.width: 1
            border.color: pycolor.outline
            color: pycolor.panel
            radius: 8
        }

        contentItem: ListView {
            anchors.fill: parent
            anchors.margins: 4
            clip: true
            model: root.model
            spacing: 2

            delegate: V.Rectangle {
                width: ListView.view.width - 8
                height: typeof modelData === 'object' && modelData.description ?
                        44 : 32
                radius: 6
                color: (
                    index === root.currentIndex ?
                    pycolor.paint_brand :
                    (mouseArea.containsMouse ?
                     pycolor.higher(pycolor.panel, 1) :
                     pycolor.transparent)
                )

                V.Text {
                    id: _label
                    anchors {
                        left: parent.left
                        leftMargin: 10
                        top: parent.top
                        topMargin: 8
                        right: parent.right
                        rightMargin: 10
                    }
                    color: (
                        index === root.currentIndex ?
                        pycolor.on_paint_brand :
                        pycolor.on_panel
                    )
                    elide: Text.ElideRight
                    font.bold: index === root.currentIndex
                    font.pixelSize: 13
                    text: typeof modelData === 'string' ?
                          modelData : modelData.label
                }

                V.Text {
                    visible: typeof modelData === 'object' &&
                             modelData.description
                    anchors {
                        left: parent.left
                        leftMargin: 10
                        top: _label.bottom
                        topMargin: 2
                        right: parent.right
                        rightMargin: 10
                    }
                    color: (
                        index === root.currentIndex ?
                        pycolor.higher(pycolor.on_paint_brand, 2) :
                        pycolor.text_secondary
                    )
                    elide: Text.ElideRight
                    font.pixelSize: 11
                    text: modelData.description
                }

                C.MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: {
                        root.currentIndex = index
                        root.selected(
                            index,
                            typeof modelData === 'string' ?
                            modelData : modelData.label
                        )
                        _popup.close()
                    }
                }
            }
        }
    }
}
