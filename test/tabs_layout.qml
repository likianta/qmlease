import QtQuick
import QmlEase
import QmlEase.Layouts

Window {
    TabsLayout {
        anchors {
            fill: parent
            margins: 48
        }
        model: ['One', 'Two', 'Three']

        Rectangle {
            // anchors.fill: parent
            color: pycolor.primary
        }

        Rectangle {
            // anchors.fill: parent
            color: pycolor.secondary
        }

        Rectangle {
            // anchors.fill: parent
            color: pycolor.tertiary
        }

        Component.onCompleted: {
            // ...
        }
    }
}
