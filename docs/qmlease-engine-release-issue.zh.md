# 记录 QmlEase 在应用退出时由 engine 释放不正确导致的大量类型警告

## 现象

关闭主程序窗口后, 控制台产生了大量的打印信息, 类似于下面的内容:

![](.assets/20221215141639.png)

## 原因

这个问题在早期的 2.0 版本中已经有了解决方案, 我们将方案表述一下:

- 在应用退出时, 会触发 `qmlease.application : Application : aboutToQuit` 信号.
- 在常规的 aboutToQuit 行为中, qt 会按照 engine 中对象的注册顺序, 逆序释放对象.
- 在对象被释放的过程中, 可能会触发对象的重构事件, 从而导致对象去引用一些已经被释放了的对象, 于是产生 `TypeError: cannot read property '...' of null` 这类警告.
- 我们在 2.0 时期的解决方法是, 主动介入 engine 的销毁过程, 这样做:

    ```python
    class Application(QApplication):

        def __init__(self, ...):
            self.aboutToQuit.connect(self._exit)
            ...

        def _exit(self):
            del self.engine
            # then release python hooks
            self._register.release()
    ```

> 以上分析来自 [这篇回答](https://bugreports.qt.io/browse/QTBUG-81247).

## 问题复现及分析

在最近的开发活动中, 我们发现原本已经被解决的该问题又重新出现.

在确认 `app._exit` 没有变化下, 我们认为是 `del self.engine` 没有成功释放导致的.

这是因为在 python 端的其他某些模块, 可能引用了 `self.engine` (或其子对象), 导致引用计数始终无法清零, 才出现了这个问题.

经过排查, 我们发现最近新增的一个模块 `qml_eval` 确实做了这件事:

```python
# qml_eval.py
from ..application import app
...

class QmlEval(...):
    def __init__(self, ...):
        self._comp = QQmlComponent(app.engine, ..., app.root.contextObject())
        #                                           ^ 这里的原因
        ...
```

将它的最后一个参数去掉后, 解决了该问题.

## 备忘

谨慎使用 `app.engine` 和 `app.root` 对象.

如果该问题在更广泛的场景中暴露, 我们将考虑重构这一块内容.
