import QtQuick
import QtQuick.Controls
import "../" as LC

ComboBox {
    id: root
    width: root._pop_item_width + icon.width
    height: root._pop_item_height
    z: root._opened ? 1 : 0

    property int    p_font_size: 11
    property alias  p_model: root.model
    property int    p_radius: 4

    property int    _anim_duration: 300 // unit: ms
    property bool   _opened: false
    property int    _pop_item_width: 0
    property int    _pop_item_height: 24

    onModelChanged: {
        //  measure popup list width and height
        var res = LKLayoutHelper.calc_model_size(root.p_model, 10, 24) // OPTM
        root._pop_item_width = res[0]
//        console.log(res, root._pop_width, root._pop_height)
    }

    component ItemText: LC.LCText {
        leftPadding: 4
        p_alignment: 'lcenter'
        p_size: root.p_font_size
    }

    background: LC.LCRectangle {
        id: bg
        border.width: 1
        border.color: '#0984d8'
        color: '#ffffff'
        height: root._opened ?
            root.height + pop.height + 12 :
            root.height // +12: add some padding space
        radius: root.p_radius

        Behavior on height {
            NumberAnimation {
                duration: root._anim_duration
                easing.type: Easing.OutQuart
            }
        }
    }

    contentItem: ItemText {
        id: txt
        p_bold: true
        p_text: root.displayText
    }

    indicator: Image {
        id: icon
        x: root.width - 24
        y: (root.height - icon.height) / 2
        width: 24
        height: 24
        rotation: root._opened ? -90 : 0
        source: RMAssets.get('arrow-drop-left-line.svg')

        Behavior on rotation {
            NumberAnimation {
                duration: root._anim_duration
                easing.type: Easing.OutQuart
            }
        }
    }

    popup: Popup {
        id: pop
//        y: root.height
//        y: root._pop_item_height
        y: root.currentIndex == 0 ?
            root._pop_item_height : root._pop_item_height + 12
            //  FIXME: don't know why its value changed.
        width: root.width
        height: root._pop_item_height * root.count

        background: Item {}
        contentItem: ListView {
            y: 90
            height: root._pop_item_height

            currentIndex: root.highlightedIndex
            model: root.model
            opacity: root._opened ? 1 : 0
            reuseItems: true
            spacing: 0

            delegate: LC.LCRectangle {
//                width: root._pop_item_width + 12
                width: pop.width - 12
                height: root._pop_item_height
                p_color: _area.p_hovered ? '#EEEEEE' : '#FFFFFF'

                ItemText {
                    id: _txt
                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    p_text: modelData
                }

                LC.LCOval {
                    anchors.right: parent.right
                    anchors.rightMargin: 4
                    anchors.verticalCenter: parent.verticalCenter
//                    x: parent.width + 2
//                    y: parent.height / 2 - 4
//                    width: 4
//                    height: 4
//                    source: RMAssets.get('checkbox-blank-circle-fill.svg')
                    visible: index == root.highlightedIndex
                    p_color: '#000000'
                    p_radius: 2
                }

                LC.LCMouseArea {
                    id: _area
                    p_hover_enabled: true
                    onClicked: {
                        root.currentIndex = index
                        pop.close()
                    }
                }
            }

            Behavior on opacity {
                NumberAnimation {
                    duration: root._anim_duration
//                    easing.type: Easing.OutQuart
                }
            }
        }

        onClosed: {
            _timer.start()
        }

        onOpened: {
            root._opened = true
        }

        Timer {
            id: _timer
            interval: root._anim_duration
            running: false
            onTriggered: {
                root._opened = false
            }
        }
    }
}