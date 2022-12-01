import QtQuick 2.15

Item {
    id: root

    property bool   demoMode: false
    property int    displayWidth
    property var    model  // optional[dict[float progress, str text]]
    property int    precision: 0  // suggest 0 or 2
    property string progColorBg: pycolor.progress_bg
    property string progColorFg: pycolor.progress_fg
    property alias  progWidth: _prog_bg.width
    property int    progHeight: 4
    property int    progRadius: progHeight / 2
    property real   progValue: 0  // usually 0.0 ~ 1.0, allow overflows.
    property int    __animDuration: 100  // 100ms
    property int    __padding: 4
    property real   __progValue  // 0.0 ~ 1.0

    signal textClicked()

    LKRectangle {
        id: _prog_bg
        anchors {
            left: parent.left
            right: _display.left
            rightMargin: root.__padding
            verticalCenter: parent.verticalCenter
        }
        height: root.progHeight
        radius: root.progRadius
        color: root.progColorBg

        LKRectangle {
            id: _prog_fg
            anchors.left: parent.left
            width: parent.width * root.__progValue
            height: parent.height
//            radius: parent.radius
            color: root.progColorFg

            Behavior on width {
                enabled: root.demoMode
                NumberAnimation {
                    duration: 200
                }
            }
        }
    }

    Loader {
        id: _test_prog
        enabled: root.demoMode
        anchors.fill: parent

        sourceComponent: MouseArea {
            anchors.fill: parent

            property var progress

            onClicked: {
                _test_timer.value = 0
                _test_timer.start()
            }

            Timer {
                id: _test_timer
                interval: 1
                repeat: true
                property real value: 0
                onTriggered: {
                    this.value += 1
                    if (this.value >= 100) {
                        this.stop()
                    }
                }
                Component.onCompleted: {
                    this.valueChanged.connect(() => {
                        progress.progValue = this.value / 100
                    })
                }
            }
        }

        onLoaded: {
            this.item.progress = root
        }
    }
    
    // ------------------------------------------------------------------------
    
    Loader {
        id: _display
        anchors {
            right: parent.right
            verticalCenter: parent.verticalCenter
        }
        width: root.displayWidth
        
        MouseArea {
            anchors.fill: parent
            onClicked: {
                root.textClicked()
            }
        }

        onLoaded: {
            if (!this.width) {
                this.width = this.item.width
            }
        }
        
        Component.onCompleted: {
            if (!root.model) {
                this.sourceComponent = _display_1
            } else {
                this.sourceComponent = _display_2
            }
        }
    }
    
    Component {
        id: _display_1
        LKText {
            property real __value: root.__progValue
    
            Behavior on __value {
                NumberAnimation {
                    duration: root.__animDuration
                }
            }
    
            Component.onCompleted: {
                this.text = lkprogress.show_value(100, root.precision)
                this.width = this.contentWidth
                this.__valueChanged.connect(() => {
                    this.text = lkprogress.show_value(
                        this.__value, root.precision
                    )
                })
                this.__valueChanged()
            }
        }
    }
    
    Component {
        id: _display_2
        LKText {
            Component.onCompleted: {
                this.width = pylayout.get_content_width(
                    this, pyside.eval(`
                        return max(map(str, model.values()),
                                   key=lambda x: len(x))
                    `, {'model': root.model})
                )
                root.__progValueChanged.connect(() => {
                    this.text = lkprogress.get_nearest_value(
                        root.__progValue, root.model
                    )
//                    console.log(root.__progValue, this.text)
                })
                root.__progValueChanged()
            }
        }
    }

    Component.onCompleted: {
        root.modelChanged.connect(() => {
//            console.log(Boolean(root.model), root.model)
            if (!root.model) {
                root.progValueChanged.connect(() => {
                    if (root.progValue > 1) {
                        root.__progValue = 1
                    } else if (root.progValue < 0) {
                        root.__progValue = 0
                    } else {
                        root.__progValue = root.progValue
                    }
                })
            } else {
                root.progValueChanged.connect(() => {
                    root.__progValue = lkprogress.get_nearest_progress(
                        root.progValue, root.model
                    )
                })
            }
        })
    }
}
