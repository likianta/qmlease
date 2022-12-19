# 安装

## 安装 QmlEase

使用 pip 即可安装:

```shell
pip install qmlease
```

当前最新版本是 3.0.0+.

注: qmlease 要求 python 3.8+ 解释器运行.

## 安装 Qt

请注意, 安装 qmlease 本体并不包含 qt 库. 你需要自行选择下面其中一个进行安装:

```shell
# pip 安装其中之一
pip install pyside6
pip install pyqt6
pip install pyside2
pip install pyqt5
```

qmlease 会自动检测你的 python 环境中安装的 qt 库 (你也可以强制指定一个). 该特性是由 [qtpy](https://github.com/spyder-ide/qtpy) 提供支持.

## 附

### 如何指定 Qt 版本 (关于 QtPy)

qtpy 为 pyside 和 pyqt 提供了一层统一的 API 来调用. 它的导入名称偏向于 pyside 的模块命名规则 (比如, `from qtpy.QtCore import Property, Signal, Slot`).

当你的 python 环境中安装了多个 qt 库, 想要指定其中一个被使用, 请在导入 qtpy 之前, 设置你的 `os.environ` 变量:

```python
import os
os.environ['QT_API'] = 'pyside6'  # pyside6, pyqt6, pyside2, pyqt5

# 然后, 导入 qtpy
from qtpy import QT_VERSION
from qtpy.QtWidgets import QWidget
print(QT_VERSION)  # e.g. '6.4.0'
print(QWidget)  # e.g. <class 'PySide6.QtWidgets.QWidget'>
```

### 为什么 QmlEase 第一个发行版从 3.0.0 开始编号

该项目前身是 [lk-qtquick-scaffold](https://github.com/likianta/lk-qtquick-scaffold), 我们在对项目启用新的命名后, 版本也从之前的 2.0 延续编号.

lk-qtquick-scaffold 项目将最终停留在 2.x 版本 (当有必要的更新时, 会逐渐填充 minor 和 patch 版本号, 但不会增加 major 版本号). 且当 qmlease 进入稳定阶段后, lk-qtquick-scaffold 将逐渐停止维护.
