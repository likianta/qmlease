import QtQuick
import QtQuick.Window
import "./LCStyle/dimension.js" as LCDimension
import "./LCStyle/palette.js" as LCPalette

Window {
    id: root
    color: LCPalette.BgWhite
    visible: true
    width: LCDimension.WinWidth; height: LCDimension.WinHeight

    property alias p_color: root.color
}
