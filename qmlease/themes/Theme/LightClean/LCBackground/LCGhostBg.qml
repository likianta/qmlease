import QtQuick 2.15
import "../LCStyle/palette.js" as LCPalette

LCRectBg {
    id: root
    // 幽灵边框, 当鼠标移到此组件上时, 才会显示边框 (并以发光效果呈现)
    p_color: LCPalette.Transparent

    property bool p_active: false
    property bool p_hovered: false  // 您需要设置父对象 (比如常见的 Button) 的
    //  hoverEnabled 属性为 true

    states: [
        State {
            when: p_hovered
            PropertyChanges {
                target: root
                p_border.width: 1
                p_color: LCPalette.TranslucentLH
            }
        }
    ]
}
