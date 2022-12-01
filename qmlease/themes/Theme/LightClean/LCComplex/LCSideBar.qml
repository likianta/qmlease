import QtQuick
import QtQuick.Controls
import ".." as LC

Item {
    id: root

    property string p_bg_color: '#E6EBF0'
    property var    p_model
    property alias  p_spacing: listview.spacing

    component MyItem: Item {
        id: _item
        height: _title.contentHeight + _padding * 2

        property string p_icon: ''
        property bool   p_selected: false
        property string p_title
        property int    _padding: 8

        signal clicked

        LC.LCRectangle {
            anchors.fill: parent
            opacity: (parent.p_selected || _area.p_hovered) ? 1 : 0
            p_color: root.p_bg_color

            Behavior on opacity {
                NumberAnimation {
                    duration: 400
                    easing.type: Easing.OutQuart
                }
            }

            LC.LCMouseArea {
                id: _area
                p_hover_enabled: true
                onClicked: _item.clicked()
            }
        }

        LC.LCIcon {
            id: _icon
            anchors.left: parent.left
            anchors.leftMargin: parent._padding
            anchors.verticalCenter: parent.verticalCenter
            p_size: _item.p_icon ? _title.contentHeight : 0
            p_source: _item.p_icon
        }

        LC.LCText {
            id: _title
            anchors.left: _icon.right
            anchors.leftMargin: _item.p_icon ? parent._padding : 0
            anchors.verticalCenter: parent.verticalCenter
            p_alignment: 'lcenter'
            p_text: _item.p_title
        }
    }

    ListView {
        id: listview
        anchors.fill: parent
        boundsBehavior: Flickable.StopAtBounds
        model: LKModelGenerator.create(
            ['m_icon', 'm_title'], root.p_model
        )
        reuseItems: true
        spacing: 8

        delegate: MyItem {
            width: listview.width
//            height: root.p_item_height ? root.p_item_height
//            implicitHeight: 120

            /*  The model example
             *
             *  ListModel {
             *      ListElement {
             *          m_icon: ''
             *          m_title: ''
             *      }
             *      ...
             *  }
             */
            p_icon: m_icon
            p_selected: index == listview.currentIndex
            p_title: m_title

            onClicked: {
                if (index == listview.currentIndex) { return }
                const is_forward = index > listview.currentIndex
                listview.currentIndex = index
                mini_indicator.start_anim(
                    this.y + this.height / 2, this.height, is_forward
                )
            }

            Component.onCompleted: {
                console.log([m_title], [this.width, this.height])
            }
        }
        
        LC.LCRectangle {
            id: mini_indicator
            anchors.top: _virtual_point_m.top
            anchors.bottom: _virtual_point_n.bottom
            x: 2
            width: 3

            p_color: '#0067C0'
            p_radius: mini_indicator.width / 2

            property bool   p_forward: true
            property int    _height: 0
            property int    _padding: 6

            function start_anim(cy1, h1, forward) {
                mini_indicator.p_forward = forward
                _virtual_point_m.y = cy1 - h1 / 2 + mini_indicator._padding
                _virtual_point_n.y = cy1 + h1 / 2 - mini_indicator._padding
            }
        }

        component VirtualPoint: Item {
            id: _point
            property int p_duration
            property int p_curve: 0

            Behavior on y {
                NumberAnimation {
                    duration: _point.p_duration
                    easing.type: _point.p_curve
                }
            }
        }

        VirtualPoint {
            id: _virtual_point_m

            p_duration: mini_indicator.p_forward ? 120 : 60
            p_curve: mini_indicator.p_forward ? 0 : Easing.OutQuart

            Component.onCompleted: {
                let item = listview.currentItem
                this.y = item.y + mini_indicator._padding
            }
        }

        VirtualPoint {
            id: _virtual_point_n

            p_duration: mini_indicator.p_forward ? 60 : 120
            p_curve: mini_indicator.p_forward ? Easing.OutQuart : 0

            Component.onCompleted: {
                let item = listview.currentItem
                this.y = item.y + item.height - mini_indicator._padding
            }
        }
    }
}
