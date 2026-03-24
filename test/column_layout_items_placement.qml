import QtQuick
import QtQuick.Layouts
import QmlEase

Window {
    RowLayout {
        anchors {
            fill: parent
            margins: 24
        }

        // i want this layout to place its children from top to bottom, the 
        // extra space should be consumed by a bottom spacer.
        Vertical {
            Layout.fillWidth: true
            Layout.fillHeight: true
            border: true
            placeItemsTop: true
            Rectangle {
                Layout.preferredWidth: 100
                Layout.preferredHeight: 100
                color: pycolor.primary
            }
            Divider {
                Layout.fillWidth: true
                horizontal: true
            }
            Rectangle {
                Layout.preferredWidth: 100
                Layout.preferredHeight: 100
                color: pycolor.secondary
            }
        }

        // i want this layout to distribute its children height equally.
        Vertical {
            Layout.fillWidth: true
            Layout.fillHeight: true
            border: true
            // placeItemsTop: true
            Rectangle {
                Layout.preferredWidth: 100
                Layout.fillHeight: true
                color: pycolor.primary
            }
            Divider {
                Layout.fillWidth: true
                horizontal: true
            }
            Rectangle {
                Layout.preferredWidth: 100
                Layout.fillHeight: true
                color: pycolor.secondary
            }
        }
    }
}