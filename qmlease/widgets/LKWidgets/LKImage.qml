import QtQuick 2.15
import QtGraphicalEffects 1.15
//import Qt5Compat.GraphicalEffects
//  "Qt5Compat.GraphicalEffects" is for qt6 (<=6.2 or >=6.4).
//  be notice that qt6.3 cannot import any of them, it's a known issue from
//  official pypi repo (see [link](https://stackoverflow.com/questions/70749269/
//  using-graphicaleffects-in-pyside6)). if you are using qt6.3, please
//  downgrade your version to 6.2 or wait for qt6.4 to be released.

Image {
    id: root

    property int radius: pysize.radius_m

    layer.enabled: radius != 0
    layer.effect: OpacityMask {
        maskSource: Rectangle {
            width: root.width
            height: root.height
            radius: root.radius
        }
    }
}
