# 操作流程

下载 pyside6-essentials 到指定目录:

```shell
cd sidework/pyside_package_tailor
pip install pyside6-essentials -t venv/qt_for_python
```

此时将得到 (示例):

```
sidework
|= pyside_package_tailor
   |= venv
      |= qt_for_python
         |= PySide6
         |= PySide6-6.4.1.dist-info
         |= shiboken6
         |= shiboken6-6.4.1.dist-info
         |= bin
```

我们将 "PySide6" 和 "shiboken6" 拷贝到 `dist/pyside6_lite` 目录下. 并在该目录下创建一个 `__init__.py` 文件:

```python
from os.path import abspath
from sys import path

_currdir = abspath(f'{__file__}/..')

init_paths = [
    f'{_currdir}/shiboken6',
    f'{_currdir}/PySide6',
]

for p in init_paths:
    path.insert(0, p)
```

于是我们得到了以下目录结构:

```
sidework
|= pyside_package_tailor
   |= dist
      |= pyside6_lite
         |= PySide6
         |= shiboken6
         |- __init__.py
```

请务必确保自己的目录结构与上述示例一致, 因为我们在接下来的脚本中使用了固定的路径.

**裁剪**

运行我们的裁剪程序:

```python
cd sidework/pyside_package_tailor

# 获取帮助
py -m pptailor -h
py -m pptailor tailor -h
py -m pptailor restore -h

# 裁剪
py -m pptailor tailor dist/pyside6_lite/PySide6
```

它将会生成:

```
sidework/pyside_package_tailor/dist
|= pyside6_lite
   |= PySide6  # 在这个目录下, 一些文件已经被 "删除" 了. 它的体积有了明显的下降.
   |= shiboken6
   |- __init__.py
|= deleted  # 所有被 "删除" 的文件, 会放在这里. 
   |# 它们在这里是平铺的结构, 多级路径被转换为 "--" 连接的顶层路径.
   |= examples
   |= plugins--sqldrivers
   |= resources
   |= translations
   |- opengl32sw.dll
   |- ...
```

**恢复**

如果要恢复, 即把 "deleted" 中的文件放回原处, 请运行:

```shell
py -m pptailor restore dist/pyside6_lite/PySide6
```

# 如何使用

用法 1: 先导入 `pyside6_lite`, 再导入 `PySide6`:

```python
import pyside6_lite

# test
import PySide6
print(PySide6.__path__)
```

用法 2: 设置环境变量 `QT_API` 为 "pyside6_lite", 然后导入 `qmlease`:

```python
import os
os.environ['QT_API'] = 'pyside6_lite'

import qmlease
print(qmlease.QT_API)

# test
import PySide6
print(PySide6.__path__)
```

# 体积降低了多少?

以 6.4.1 为例观察:

- 原始体积
  - whl 文件: 77mb
  - 解压后: 195mb
- 裁剪后
  - 压缩前: 102mb
  - 普通压缩后: 34.5mb
  - 极限压缩后: 21mb

# 测试

- 在 `depsland/build/setup_wizard` 中测试通过.
- 在 `(private_project)/eye_diagram` 中测试通过.
