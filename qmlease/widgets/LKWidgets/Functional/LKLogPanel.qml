import QtQuick 2.15
import "../Buttons" as B

Rectangle {
    id: root
    clip: true
    color: pycolor.panel_bg
    radius: pysize.radius_m

    property string placeholder: 'The logging message will be shown here'
    property string __fontFamily: lkutil.get_monospaced_font()

    function log(msg) {
        lklogger.qlog(msg)
    }

    Text {
        id: _placeholder
        visible: !Boolean(_view.count)
        anchors.centerIn: parent
        color: pycolor.text_hint
        font.family: pyfont.font_default
        font.pixelSize: pyfont.size_m
        text: root.placeholder
        wrapMode: Text.Wrap
    }

    ListView {
        // use ListView rather than TextArea better for performance.
        //  https://stackoverflow.com/questions/31345096/textarea-slow-for
        //  -logging
        id: _view
        anchors {
            fill: parent
            leftMargin: 8
            rightMargin: 8
            topMargin: 4
            bottomMargin: 2
        }
        boundsBehavior: Flickable.StopAtBounds
        clip: true
        model: lklogger.get_model()
        delegate: Text {
            width: _view.width
            color: pycolor.text_main
            font.family: root.__fontFamily
            font.pixelSize: 11
            text: model['msg']
            textFormat: Text.RichText
            wrapMode: Text.WrapAnywhere
        }

        onCountChanged: {
//            _view.currentIndex = _view.count - 1
            _view.positionViewAtEnd()
        }
    }

    B.LKIconButton {
        id: _clear
        visible: Boolean(_view.count)
        anchors {
            right: parent.right
            top: parent.top
            margins: pysize.margin_l
        }
        bgColor: pycolor.button_bg_hovered
        color: hovered ? pycolor.red_5 : pycolor.icon_line_default
        halo: true
        size: 18
        source: pyassets.get('lkwidgets', 'Assets/delete-bin-2-line.svg')
        onClicked: lklogger.clear()
    }
}
