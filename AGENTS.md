# AGENTS.md

## 这是什么项目

本项目是基于 PySide6 + QML 创建的 GUI 框架, 它包含大量的功能模块, 和一套预设的 QML 组件库. 这些功能仍在积极开发中.

请注意, 由于本项目的开发周期非常长, 有大量历史原因堆积的模块处于少量报错或完全不可用的状态, 在开发时需要甄别.

## 项目目录结构

```yaml
.venv/: 本项目的 Python 虚拟环境, 使用 uv 创建. Python 版本为 3.14.
blueprint/: 已废弃的目录, 可忽略.
docs/: 开发文档和备忘.
examples/:
  # 该目录展示了可运行和演示的应用示例, 值得注意的是大部分示例已经停止维护且会报错, 只有下面列出的是最新添加且可用的.
  sidebar/: 侧边栏示例.
  click_counter.qml: 点击计数器示例.
gallery/: 一些应用截图.
lib/:
  qmlease_colorsys/: 专为 QmlEase 设计的颜色生成系统.
prototype/: 设计原型图, 可作为组件设计参考. 一般是 HTML 或 PNG 文件.
qmlease/: # 项目源代码
  application/:
    application.py: 对 QApplication 的封装.
    register.py: 注册 QObject 对象到 QML 上下文.
  declarative/: 暂时停止维护, 可忽略.
  experimental_features/: 暂时停止维护, 可忽略.
  pyside/: 与 `application.register` 相关的模块.
  qmlside/: # 与 QML 相关的模块.
    hot_reloader/: 热重载功能.
    layout_engine/: 布局引擎, 暂时停止维护, 仅供参考.
    model/: 目前主要在用的是 list_model 模块.
    resource_manager/: 资源枚举值 (例如 padding_xs, padding_l, font_size_xs, ...), 已停止维护, 可忽略.
    widgets_backend/: 已停止维护, 可忽略.
    assets.py: 用来索引资源路径.
    console.py: 将 QML 端的打印重定向到 Python 控制台.
  qtcore/: 对 QObject, Signal, Slot 等核心概念的封装.
  style/: 样式相关的模块. 重点关注 color3.py, 它与 lib/qmlease_colorsys/ 相关.
  widget_support/: 由于 ./qmlside/widgets_backend/ 已停止维护, 这是第二代重构后的模块, 但同样缺少维护, 谨慎使用.
  widgets/:
    # QML 组件库
    LKWidgets/: 已停止开发, 可忽略.
    QmlEase/: 
      # 主要组件库, 积极开发中. 每个子目录都会有一个 qmldir 文件.
      Composites/: 多种基础组件组合而成的复杂组件.
      Inputs/: 输入型组件.
      Layouts/: 布局类组件.
      Visual/: 可视化组件.
      qmldir: 该索引只列出常用的组件. 对于非常用的组件, 需要通过 `import QmlEase.<SubModule>` 来导入.
references/:
  omnicomm_serdes_tool/: 第三方项目, 基于 QmlEase 框架完整开发, 可作为代码用法的重要参考.
sidework/: 一些周边工作.
test/: 测试模块.
unittests/: 旧的测试模块, 将会被逐渐转移到 test/ 目录下.
pyproject.toml: 我们使用现代的 Python 项目管理方式 (uv + ruff + ty).
```

## 工具链

- 使用 `python` 运行脚本.
- 使用 `uv` 管理 pyproject.toml 中的依赖.
- 使用 `ty` 检查 ".py" 文件的类型错误.
- 使用 `ruff` 格式化 ".py" 文件的代码.
- 使用 `python tools/qmllint.py check` 检查 ".qml" 文件的代码. (实验性功能)

如果要运行一个应用, 有两种方法:

1. 如果有 py 脚本作为入口, 则通过 `python <py_file>` 启动.
2. 如果没有 py 脚本, 只有一个 qml 文件作为入口, 则通过 `python -m qmlease run <qml_file>` 启动.

## 代码风格 (Python)

- 优先使用 `format` 而不是 `f-string`.
- 代码中使用全英文, 不要有中文注释.
- 在代码注释 (`#` 开头的注释), `print(...)` 以及 `Exception(...)` 中使用小写字母开头的句子. 在函数注解 (docstring) 中, 则使用规范的大小写格式.
- 不需要在入口脚本的顶部添加 `sys.path.append(...)`. 因为我们已经设置好了环境变量 `PYTHONPATH=.;src;lib;.venv/Lib/site-packages`.
- 优先使用 qmlease 提供的模块

  例如:
  - 优先使用 `qmlease.app` 而不是 `QApplication`
  - 优先使用 `qmlease.app.register(...)` 而不是 `<some_qml_engine>.rootContext().setRootContext(...)`
  - 优先使用 `qmlease.assets.get(...)` 而不是 `qrc:/...`
  - 优先使用 `qmlease.Signal/Slot` 而不是 `PySide6.QtCore.Signal/Slot`
  - 优先使用 `qmlease.QObject` 而不是 `PySide6.QtCore.QObject`
  - ...

  如果不确定用法, 可自己阅读代码理解, 或者参考 examples/, test/ 以及 references/omnicomm_serdes_tool/ 中的示例帮助自己理解.

- 优先使用 qmlease/widgets/QmlEase/ 提供的组件.

  例如:
  - 优先使用 `QmlEase.Rectangle` 而不是 `QtQuick.Rectangle`
  - 优先使用 `QmlEase.Text` 而不是 `QtQuick.Text`
  - 优先使用 `QmlEase.Button` 而不是 `QtQuick.Controls.Button`
  - 优先使用 `QmlEase.Row/Column` 而不是 `QtQuick.Layouts.RowLayout/ColumnLayout`
  - 优先使用 `pycolor` 提供的颜色, 而不是自己硬编码 `red` `blue` `#efefef` 之类的颜色
  - ...

  如果组件功能不完善, 请帮助完善它们.

- 每行代码不超过 80 字符 (见 `pyproject.toml:[tool.ruff]:line-length`).
- 每当完成修改后, 使用 `ty check`, `ruff check`, `ruff format` 等命令检查代码风格.

## 代码风格 (QML)

- 代码中使用全英文, 不要有中文注释.
