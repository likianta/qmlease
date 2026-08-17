import QtQuick
import QtQuick as Q
import QmlEase

Window {
    Rectangle {
        id: rect1
        x: 20
        y: 20
        width: 100
        height: 40
        color: pycolor.paint_brand

        Behavior on width {
            NumberAnimation {
                duration: 1000
            }
        }
    }

    Row {
        x: 20
        y: 80
        color: pycolor.container_tint
        hpadding: 24

        Rectangle {
            id: rect2
            width: 80
            height: 40
            color: pycolor.paint_info
        }

        Rectangle {
            id: rect3
            width: 80
            height: 40
            color: pycolor.paint_error

            // Behavior on width {
            //     NumberAnimation {
            //         duration: 1000
            //     }
            // }
        }

        // Behavior on width {
        //     NumberAnimation {
        //         duration: 1000
        //     }
        // }
        // Behavior on backgroundWidth {
        //     NumberAnimation {
        //         duration: 1000
        //     }
        // }
        Behavior on implicitWidth {
            NumberAnimation {
                duration: 1000
            }
        }
    }

    Q.Row {
        x: 20
        y: 140
        // height: 40
        clip: true
        leftPadding: 24
        rightPadding: 24
        spacing: 4

        Rectangle {
            id: rect4
            width: 80
            height: 40
            color: pycolor.paint_success
        }
        
        Rectangle {
            id: rect5
            width: 80
            height: 40
            color: pycolor.paint_warning

            Behavior on width {
                NumberAnimation {
                    duration: 1000
                }
            }
        }

        Behavior on width {
            NumberAnimation {
                duration: 1000
            }
        }
        // Behavior on implicitWidth {
        //     NumberAnimation {
        //         duration: 1000
        //     }
        // }

        // Component.onCompleted: {
        //     pylayout.inspect_size(this, 'Q.Row')
        // }
    }

    Button {
        x: 20
        y: 200
        text: 'Change width'
        onClicked: {
            rect1.width = rect1.width == 100 ? 200 : 100
            // rect2.width = rect2.width == 80 ? 160 : 80
            rect3.width = rect3.width == 80 ? 160 : 80
            // rect4.width = rect4.width == 80 ? 160 : 80
            rect5.width = rect5.width == 80 ? 160 : 80
        }
    }
}