import QtQuick
import "../Controls" as C
import "../Layouts" as L
import "../Visual" as V

L.Row {
    id: root
    implicitHeight: 36
    valign: 'center'
    lpadding: 16
    rpadding: 24
    // vpadding: 4
    spacing: 8

    borderColor: (
        status == 'idle' ?
        pycolor.container :
        status == 'info' ?
        pycolor.outline_info :
        status == 'success' ?
        pycolor.outline_success :
        status == 'warning' ?
        pycolor.outline_warning :
        status == 'error' ?
        pycolor.outline_error :
        pycolor.container
    )
    // borderWidth: 1
    color: (
        status == 'idle' ?
        pycolor.container :
        status == 'info' ?
        pycolor.container_info :
        status == 'success' ?
        pycolor.container_success :
        status == 'warning' ?
        pycolor.container_warning :
        status == 'error' ?
        pycolor.container_error :
        pycolor.container
    )

    property int    maxTextWidth: 0
    property string status: 'idle' // idle, info, success, warning, error
    property string text: (
        status == 'idle' ?
        'IDLE' :
        status == 'info' ?
        'INFO' :
        status == 'success' ?
        'SUCCESS' :
        status == 'warning' ?
        'WARNING' :
        status == 'error' ?
        'ERROR' :
        'IDLE'
    )
    // property string _indicatorColor: status == 'idle' ? 
    //     pycolor.text_tertiary : _textColor
    property string _indicatorColor: (
        status == 'idle' ?
        pycolor.text_tertiary :
        status == 'info' ?
        pycolor.paint_info :
        status == 'success' ?
        pycolor.paint_success :
        status == 'warning' ?
        pycolor.paint_warning :
        status == 'error' ?
        pycolor.paint_error :
        pycolor.text_tertiary
    )
    property string _textColor: (
        status == 'idle' ?
        pycolor.text_secondary :
        status == 'info' ?
        pycolor.on_container_info :
        status == 'success' ?
        pycolor.on_container_success :
        status == 'warning' ?
        pycolor.on_container_warning :
        status == 'error' ?
        pycolor.on_container_error :
        pycolor.text_secondary
    )

    function measureTextWidth(text) {
        return textMetrics.getTextLength(text)   
    }

    onTextChanged: {
        root.computeLayout()
    }

    Behavior on color {
        ColorAnimation {
            duration: 100
        }
    }

    Behavior on _indicatorColor {
        ColorAnimation {
            duration: 100
        }
    }

    Behavior on _textColor {
        ColorAnimation {
            duration: 100
        }
    }

    V.Circle {
        size: 12
        color: root._indicatorColor
    }

    Item {
        implicitWidth: root.maxTextWidth > 0 ? 
            root.maxTextWidth : textItem.implicitWidth
        implicitHeight: textItem.implicitHeight

        V.Text {
            id: textItem
            // width: root.maxTextWidth > 0 ? root.maxTextWidth : implicitWidth
            color: root._textColor
            text: root.text

            C.TextMetrics {
                id: textMetrics
                target: parent
                // Component.onCompleted: {
                //     console.log(
                //         'max width of status indicator', 
                //         this.getTextLength('SUCCESS') // -> 50.66
                //     )
                // }
            }
        }
    }
}
