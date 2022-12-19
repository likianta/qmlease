# 样式管理器 (WIP)

qmlease 提供了一系列风格/样式控制器, 如下所示:

| 样式 | 描述 |
| ---- | ---- |
| `pycolor`  | 色彩相关定义. |
| `pyfont`   | 字体相关定义. |
| `pysize`   | 尺寸, 边缘, 间距等定义. |
| `pymotion` | 动画相关的定义 (动画时长, 动画曲线等). |

## 使用方法 (示例)

```qml
import QtQuick

Window {
    visible: true
    
    Rectangle {
        width: pysize.panel_width
        height: pysize.panel_height
        color: pycolor.panel_bg
        border.width: 1
        border.color: pycolor.panel_border
    }
}
```
