import QtQuick 2.15
import ".."
import "../Buttons"

LKRectangle {
    id: root
    width: pysize.sidebar_width
    height: pysize.sidebar_height
    clip: true
    color: root.colorBg

    property string colorBg: pycolor.sidebar_bg
    property string colorItemBg: pycolor.sidebar_bg
    property string colorItemBgHovered: pycolor.button_bg_hovered
    property string colorItemBgSelected: pycolor.button_bg_pressed
    property string colorItemIcon: pycolor.icon_line_default
    property string colorItemIconSelected: pycolor.icon_line_default
    property string colorItemText: pycolor.text_default
    property string colorItemTextSelected: pycolor.text_default
    property alias  currentIndex: _listview.currentIndex
    property alias  currentItem: _listview.currentItem
    property int    itemHeight: pysize.button_height_l
    property alias  listview: _listview
    property alias  model: _listview.model
    //  union[list[str], list[dict]]
    //      for list[dict]:
    //          required keys:
    //              text: str
    //          optional keys:
    //              icon: str
    //              color: str
    property bool  reuseItems: true

    signal clicked(int index, string text)

    ListView {
        id: _listview
        anchors {
            fill: parent
            leftMargin: pysize.margin_m
            rightMargin: pysize.margin_m
            topMargin: pysize.margin_xl
            bottomMargin: pysize.margin_xl
        }
        reuseItems: root.reuseItems
        spacing: pysize.spacing_m

        delegate: LKButton {
            id: _item
            width: _listview.width
            height: root.itemHeight
            bgColorDefault: root.colorItemBg
            bgColorHovered: root.colorItemBgHovered
            bgColorPressed: root.colorItemBgSelected
            border.width: 0
            text: __data['text']
            textItem.color: _item.selected ?
                root.colorItemTextSelected : root.colorItemText
            textItem.horizontalAlignment: Text.AlignLeft
            textItem.leftPadding: __data['icon'] ?
                pysize.icon_size_l + pysize.margin_l * 2 : pysize.spacing_m

            property int  index: model.index
            property bool selected: model.index == _listview.currentIndex
            // property var  __data: {'text': '', 'icon': '', 'color': ''}
            property var  __data: py.qmlease.fill_sidebar_item(modelData)

            onClicked: {
                root.clicked(this.index, this.text)
                _listview.currentIndex = this.index
            }

            LKIcon {
                id: _icon
                visible: __data['icon']
                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                    margins: pysize.margin_m
                }
                color: _item.selected ?
                    root.colorItemIconSelected : root.colorItemIcon
                size: pysize.icon_size_l
                source: __data['icon']
            }

            Component.onCompleted: {
                this.color = Qt.binding(() => {
                    if (this.selected) {
                        return this.bgColorPressed
                    } else if (this.hovered) {
                        return this.bgColorHovered
                    } else {
                        return this.bgColorDefault
                    }
                })
            }
        }
    }
}
