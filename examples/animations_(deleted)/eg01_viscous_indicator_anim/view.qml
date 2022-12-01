import QtQuick
import LightClean
import LightClean.LCComplex

LCWindow {
    width: 280
    height: 360

    LCSideBar {
        anchors.fill: parent

        // icon from: https://iconduck.com/sets/bubblecons-nations-icon-set
        p_model: [
            {m_title: 'Sprint', m_icon: 'file:stopwatch.svg'},
            {m_title: 'Boomerang', m_icon: 'file:boomerang.svg'},
            {m_title: 'Football', m_icon: 'file:football-spain.svg'},
        ]
    }
}
