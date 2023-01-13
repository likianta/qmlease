import QtQuick 2.15
import QtQuick.Controls 2.15
import ".."

Item {
    id: root
    width: 0
    height: pysize.button_height
    clip: false

    property string colorBgDefault: pycolor.panel_bg
    property string colorBgHovered: pycolor.button_bg_hovered
    //  or pycolor.button_bg_hovered
    property string colorBgPressed: pycolor.button_bg_pressed
    property int    currentIndex: 0
    property alias  displayText: _display.text
    property int    dropdownHeight: 0
    property string dropdownBgColor: colorBgDefault
    property string dropdownBorderColor: _display.border.color
    property bool   expandable: true
    property alias  expanded: _dropdown.opened
    //  this is readonly. it is controled by _dropdown's opened and closed
    //  signal.
    property bool   editable: false  // TODO
    property int    indicatorSize: pysize.indicator_size
    property var    model  // list[str]
    property bool   wheelEnabled: true
    property bool   wheelLoop: false
    property int    __padding: pysize.padding_m

    signal selected(int index, string text)

    component MyItem: LKRectangle {
        width: root.width
        height: pysize.button_height
        border.width: 0
        border.color: pycolor.border_default
        color: {
            if (root.expandable) {
                if (_area.containsPress) {
                    return root.colorBgPressed
                } else if (_area.containsMouse) {
                    return root.colorBgHovered
                } else {
                    return root.colorBgDefault
                }
            } else {
                return root.colorBgDefault
            }
        }

        property alias  hovered: _area.containsMouse
        property alias  pressed: _area.containsPress
        property string text
        property alias  textItem: _text

        signal clicked()

        LKText {
            id: _text
            anchors {
                left: parent.left
                leftMargin: root.__padding
                verticalCenter: parent.verticalCenter
            }
            color: root.expandable ?
                pycolor.text_default : pycolor.text_disabled
            text: parent.text
        }

        MouseArea {
            id: _area
            anchors.fill: parent
            hoverEnabled: true
            onClicked: parent.clicked()
            onWheel: (whl) => {
                if (root.wheelEnabled) {
                    // we should use `var` here, not `let` or `const`.
                    // this is a bug in qt 5 and qt 6.0~6.1. see also
                    //  https://bugreports.qt.io/browse/QTBUG-91917
                    var delta = -Math.round(whl.angleDelta.y / 120)
                    var nextIndex = root.currentIndex + delta
                    if (nextIndex < 0) {
                        if (root.wheelLoop) {
                            nextIndex = root.model.length - 1
                        } else {
                            nextIndex = 0
                        }
                    } else if (nextIndex >= root.model.length) {
                        if (root.wheelLoop) {
                            nextIndex = 0
                        } else {
                            nextIndex = root.model.length - 1
                        }
                    }
                    if (root.currentIndex != nextIndex) {
                        root.currentIndex = nextIndex
                    }
                }
            }
        }
    }

    MyItem {
        id: _display
        border.width: 1
        text: root.model[root.currentIndex]

        onClicked: {
            if (root.expandable) {
                if (root.expanded) {
                    _dropdown.close()
                } else {
                    _dropdown.open()
                }
            }
        }

        LKIcon {
            id: _indicator
            anchors {
                right: parent.right
                rightMargin: root.__padding
                verticalCenter: parent.verticalCenter
            }
            rotation: root.expanded ? 0 : 90
            size: root.indicatorSize
            source: '.assets/chevron-down-arrow.svg'
    //        sourceSize.width: root.indicatorSize - 2  // -2 for better appearance
    //        sourceSize.height: root.indicatorSize
            Behavior on rotation {
                NumberAnimation {
                    duration: 100
                }
            }
        }
    }

    Popup {
        id: _dropdown
        y: _display.height + root.__padding
        width: root.width
        height: root.dropdownHeight
        clip: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent

        background: LKRectangle {
            width: parent.width
            height: root.expanded ? parent.height : 0

            border.width: 1
            border.color: root.dropdownBorderColor
            color: root.dropdownBgColor

            Behavior on height {
                NumberAnimation {
                    duration: 100
                }
            }
        }

        contentItem: LKListView {
            anchors.fill: parent
            anchors.margins: pysize.margin_s
            model: root.model
            spacing: pysize.spacing_s

            delegate: MyItem {
                text: modelData
                property int index: model.index
                onClicked: {
                    root.currentIndex = this.index
                    root.selected(this.index, this.text)
                    _dropdown.close()
                }
            }
        }

        Component.onCompleted: {
            if (this.height == 0) {
                const totalHeight = (
                    pysize.margin_s * 2 +
                    pysize.button_height
                ) * root.model.length + (
                    pysize.spacing_m * (root.model.length - 1)
                )
                if (totalHeight > pysize.listview_height) {
                    this.height = pysize.listview_height
                } else {
                    this.height = totalHeight
                }
            }
        }
    }

    Component.onCompleted: {
        if (this.width == 0) {
            // get longest item of model
            const longestContent = pyside.eval(`
                return max(map(str, model), key=len)
            `, {'model': root.model})
//            console.log(longestContent)

            _display.text = longestContent
            this.width = (
                _display.textItem.contentWidth +
                root.indicatorSize +
                root.__padding * 3
            ) * 1.5

            // restore text binding
            _display.text = root.model[root.currentIndex]
            _display.text = Qt.binding(() => {
                return root.model[root.currentIndex]
            })
        }
    }
}
