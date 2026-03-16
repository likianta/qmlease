import QtQuick
import QmlEase
import QmlEase.Layouts

Window {
    TabsLayout {
        anchors {
            fill: parent
            margins: 48
        }
        model: ['One', 'Two', 'Three Four Five']

        Rectangle {
            color: pycolor.primary
        }

        Rectangle {
            color: pycolor.secondary
        }

        Rectangle {
            color: pycolor.tertiary
        }
    }
}
