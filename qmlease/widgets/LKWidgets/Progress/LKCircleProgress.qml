import QtQuick 2.15
import ".."

Item {
    id: root
    width: circleSize
    height: circleSize

    readonly property alias canvas: _canvas
    readonly property alias textItem: _text

    property int    animateValueDuration: 100
    property int    circleSize: 100
    property string color0: 'transparent'
    property string color1: pycolor.progress_bg
    property string color2: pycolor.progress_fg
    property int    holoRadius: 0
    property real   offset: 0
    property int    ringSize: 8
    property real   value: 0  // 0.0 - 1.0

    property real   _angle: 2 * Math.PI * _safeValue
    property real   _safeValue: Math.min(Math.max(value, 0), 1)

    on_SafeValueChanged: _canvas.requestPaint()

    Behavior on _safeValue {
        NumberAnimation {
            duration: root.animateValueDuration
            //  this is an easeing duration, but for some high frequent updates
            //  it doesn't look well, you can reduce the value in your need.
        }
    }

    // https://blog.csdn.net/gongjianbo1992/article/details/122870986
    Canvas {
        id: _canvas
        anchors {
            fill: parent
//            centerIn: parent
        }

        property real radius: width / 2

        onPaint: {
            let ctx = _canvas.getContext('2d')
            ctx.clearRect(0, 0, _canvas.width, _canvas.height)
            ctx.lineCap = 'round'
            drawBg(ctx)
            drawFg(ctx)
        }

        // context.arc(x, y, r, angle_start, angle_end, clockwise)
        //  x: the x coordinate of the center of the circle.
        //  y: the y coordinate of the center of the circle.
        //  r: the radius of the circle.
        //  angle_start: the starting angle, in radians (0 is at the 3 o'clock
        //      position of the arc's circle).
        //  angle_end: the ending angle, in radians.
        //  clockwise: optional. set true is anti-clockwise.
        function drawBg(ctx) {
            const color_offset = root.offset > Math.PI ?
                (1 - (root.offset - Math.PI) / Math.PI) :
                (root.offset / Math.PI)

            ctx.beginPath()
            ctx.arc(
                _canvas.width / 2,
                _canvas.height / 2,
                _canvas.radius - root.ringSize / 2 - root.holoRadius,
                0,
                2 * Math.PI
            )
            ctx.lineWidth = root.ringSize + root.holoRadius * 2
            ctx.strokeStyle = root.color1
            ctx.stroke()

//            ctx.beginPath()
//            ctx.arc(
//                _canvas.width / 2,
//                _canvas.width / 2,
//                _canvas.radius - root.ringSize / 2 - root.holoRadius,
//                0,
//                2 * Math.PI
//            )
//            ctx.lineWidth = root.ringSize
//            ctx.strokeStyle = Qt.lighter(root.color1, 1.6 + 0.2 * color_offset)
//            ctx.stroke()
        }

        function drawFg(ctx) {
            // ctx.save()
            // the shadow effect consumes high cpu.
            // ctx.shadowColor = root.color2
            // ctx.shadowBlur = root.ringSize / 4
            ctx.beginPath()
            ctx.arc(
                _canvas.width / 2,
                _canvas.width / 2,
                _canvas.radius - root.ringSize / 2 - root.holoRadius,
                0,
                root._angle,
                false,  // clockwise
            )
            ctx.lineWidth = root.ringSize + root.holoRadius * 2
            ctx.strokeStyle = root.color2
            ctx.stroke()
            // ctx.restore()
        }
    }

    LKText {
        id: _text
        anchors { centerIn: parent }
        font.pixelSize: root.circleSize / 3.5
        color: root.color2
        text: `<font size="32">${Math.round(root._safeValue * 100)}</font>` +
              `<font size="24">%</font>`
    }
}
