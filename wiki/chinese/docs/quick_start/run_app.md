# 运行第一个 QML 应用

一个最简单的 qml 应用, 由一个 py 文件和一个 qml 文件组成:

```
simple_app_demo
|- main.py
|- view.qml
```

在 "main.py" 中, 我们引入 `qmlease.app` 来执行一个 qml 文件:

```python
from qmlease import app
app.run('view.qml')
```

在 "view.qml" 中:

> 注: 我们使用的是 qt6 的 qml 语法.

```qml
import QtQuick

Window {
    title: 'A simple application'
    visible: true
    width: 400
    height: 300

    Text {
        anchors.centerIn: parent
        text: 'Hello World'
    }
}
```

运行截图:

![](../images/20221219160315.png)
