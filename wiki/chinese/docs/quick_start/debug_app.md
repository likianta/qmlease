# 以调试模式运行 QML 应用

开启调试模式非常简单. 基于我们上个例子中的 "main.py", 我们只需要在 `app.run` 中添加一个 `debug=True` 参数即可:

```python
from qmlease import app
app.run('view.qml', debug=True)
```

再次运行, 会在屏幕的右侧出现一个 "RELOAD" 按钮, 每当我们修改了 "view.qml" 中的内容, 点击 "RELOAD" 即可刷新界面:

![](../images/20221219161609.gif)

如何关闭应用:

"RELOAD" 按钮是以窗口置顶的形式出现的. 在 windows 端, 按下 `alt + f4` 来停止; 在 macos 端, 点击关闭按钮来停止.
