import QtQuick 2.0

Item {
    property int  animateValueDuration: 100
    property real value: 0  // 0.0 - 1.0, allow overflows
    property real _safeValue: Math.min(Math.max(value, 0), 1)

    Behavior on _safeValue {
        NumberAnimation {
            duration: root.animateValueDuration
            //  this is an easeing duration, but for some high frequent updates
            //  it doesn't look well, you can reduce the value in your need.
        }
    }
}
