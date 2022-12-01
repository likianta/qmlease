import QtQuick 2.15
import QtQuick.Controls 2.15

import "../"
import "../LCBackground"
import "../LCStyle/dimension.js" as LCDimension
import "../LCStyle/motion.js" as LCMotion
import "../LCStyle/palette.js" as LCPalette

CheckBox {
    id: root
    // implicitWidth: LCDimension.ButtonWidthM
    implicitHeight: LCDimension.ButtonHeightS
    hoverEnabled: true
    leftPadding: LCDimension.HSpacingM
    rightPadding: LCDimension.HSpacingS

    property alias p_text: root.text
    property alias p_active: root.checked

    background: LCGhostBg {
        p_active: root.p_active
        p_hovered: root.hovered
    }

    contentItem: LCText {
        id: _txt
        anchors.left: _indicator.right
        anchors.leftMargin: LCDimension.HSpacingS
        p_alignment: "vcenter"
        p_color: root.enabled ? LCPalette.TextNormal : LCPalette.TextDisabled
        p_text: root.text
    }

    indicator: LCCheckBoxIndicatorBg {
        id: _indicator
        anchors.left: parent.left
        anchors.leftMargin: LCDimension.HSpacingS
        anchors.verticalCenter: parent.verticalCenter

        p_active: root.p_active

        Image {
            anchors.fill: parent
            anchors.margins: LCDimension.SpacingS
            source: '../rss/check-white.svg'
            visible: parent.p_active
        }
    }

    Component.onCompleted: {
        root.implicitWidth = root.leftPadding + root.rightPadding +
            (_txt.x + _txt.implicitWidth - _indicator.x)
    }
}