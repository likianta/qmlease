""" README.zh.md

# 资源管理器

创建跨主题的, 通用的资源管理. 在 QML 中通过 `R<ManagerName>.get(<name>)` 获取.

# 特性

- 全局管理
- 动态生成
- 回调

# 示例

```qml
import QtQuick

Rectangle {
    width: RShape.get('width-m')
    height: RShape.get('height-m')
    color: RColor.get('theme-accent')
}
```

# 领域

- Color
- Control
- Layout
- Motion
- Resource
- Shape
- Text

# 高级用法

## 自动推断

TODO

"""
from .assets import AssetsResourceManager
from .base import BaseResourceManager
from .color import ColorResourceManager
from .control import ControlResourceManager
from .layout import LayoutResourceManager
from .motion import MotionResourceManager
from .shape import ShapeResourceManager
from .text import TextResourceManager
