import QtQuick
import LKWidgets

LKWindow {
    id: root
    objectName: 'view#root'
    width: 600
    height: 800
    color: '#eeeeee'  // f2f2f2 | eeeeee

    property string imgFile: ''

    LKColumn {
        id: _container
        anchors {
            fill: parent
            margins: 20
        }

        LKRow {
            width: parent.width
            height: 160
            alignment: 'vfill'
            autoSize: true

            LKRectangle {
                id: _profile
                width: 0.5
                color: 'transparent'

                LKColumn {
                    anchors {
                        fill: parent
                    }
                    LKText {
                        horizontalAlignment: Text.AlignLeft
                        color: '#333333'
                        font.bold: true
                        font.pixelSize: 24
                        text: 'Mara bleak, mara sercious...'
                    }
                }
            }

            Loader {
                id: _miniCard
                width: 0.5
                // sourceComponent: _imgCard
                Component.onCompleted: {
                    this.xChanged.connect(_fullCard.initLocation)
                }
            }
        }
    }

    Component {
        id: _imgCard

        LKRectangle {
            id: _imgFrame
            // width: 0.5
            // clip: true
            color: '#234471'

            layer.enabled: true  // true|false
//            layer.effect: OpacityMask {
//                maskSource: Rectangle {
//                    width: _imgFrame.width
//                    height: _imgFrame.height
//                    radius: _imgFrame.radius
//                }
//            }

            Image {
                id: _img
                anchors {
                    // centerIn: parent
                    horizontalCenter: parent.horizontalCenter
                }
                // width: parent.width
                height: parent.height + floatingOffset
                fillMode: Image.Pad
                source: root.imgFile
                visible: true

                property bool expanded: false
                property int  floatingOffset: 30
                property bool hovered: _area.containsMouse

                function switchFloatable() {
                    _img.expanded = !_img.expanded
                }

                states: [
                    State {
                        when: _img.hovered & !_img.expanded
                        PropertyChanges {
                            target: _img
                            y: _imgFrame.y - floatingOffset
                        }
                    }
                ]

                transitions: [
                    Transition {
                        NumberAnimation {
                            duration: 1000
                            easing.type: Easing.OutQuart
                            properties: "y"
                        }
                    }
                ]
            }

            MouseArea {
                // When the mouse hovered, floating background image
                id: _area
                anchors.fill: parent
                hoverEnabled: true

                Component.onCompleted: {
                    this.clicked.connect(_fullCard.expand)
                    this.clicked.connect(_img.switchFloatable)
                }
            }
        }
    }

    Loader {
        id: _fullCard
        x: __initX
        y: __initY
        z: 1
        width: _miniCard.width
        height: _miniCard.height
        sourceComponent: _imgCard

        property bool shown: false
        property int  __initX: 0
        property int  __initY: 0

        function initLocation() {
            // ??????: _miniCard.onCompleted ???, ???????????????????????? (x=0, y=0); ???
            // _miniCard.xChanged ???, ??????????????????????????? (x=280, y=0).
            const coord = _miniCard.mapToItem(null, 0, 0)
            _fullCard.__initX = coord.x
            _fullCard.__initY = coord.y
//            console.log(coord.x, coord.y)
        }

        function expand() {
            _fullCard.shown = !_fullCard.shown
        }

        states: [
            State {
                when: _fullCard.shown
                PropertyChanges {
                    target: _fullCard
                    width: root.width + 10
                    //  root.width + 10 | _root.width | _container.width
                    height: root.height + 10
                    //  root.height + 10 | _root.height | _container.height
                    x: -5  // -5 | 0 | _container.x
                    y: -5  // -5 | 0 | _container.y
                    /*        ^A   ^B  ^C
                        A: ???????????? _imgMask ???????????? root ???????????????????????????????????????,
                           ?????????????????????????????????????????????
                        B: ???????????? A ?????????, ????????????????????????
                        C: ?????? _container ???????????????, ?????? A ???????????????
                     */
                }
            }
        ]

        transitions: [
            Transition {
                NumberAnimation {
                    duration: 600
                    easing.type: Easing.OutQuart // InOutQuad | OutQuart
                    properties: 'width, height, x, y'
                }
            }
        ]
    }

    Component.onCompleted: {
        this.imgFile = './test_image.jpg'
//        this.imgFile = './test_image_2.gif'
    }
}
