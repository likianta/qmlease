# QmlEase: 快速构建基于 QML 的现代化桌面应用框架

qmlease 是为 python 开发者提供的 qml 可视化界面快速构建方案. 它在 python 端封装了大量模块, 以实现良好的 python-qml 交互开发体验.

qmlease 主要特性如下:

- 支持 pyside6/pyqt6/pyside2/pyqt5 (基于 [qtpy](https://github.com/spyder-ide/qtpy)).
- 简单的几行代码, 启动 qml 应用.
- 热重载工具, 方便 qml 布局的快速调试.
- 更加简洁, 优雅的 `signal` `slot` 语法风格.
- 更好的注册机制, 实现 python 与 qml 的互操作. (且更加偏重于在 python 端实现复杂的逻辑.)
- 在 python 控制台显示 qml `console` 打印的信息.
- 预置一套开箱即用的组件库, 在动画, 视觉, 交互体验等方面经过精心设计. (更多组件/主题库在开发中!)
- 增强的布局引擎.
- 支持自动补全的样式表.

qmlease 于 2022 年 12 月正式发布了它的第一个 3.0.0 版本[^1], 现在可以通过 [pypi 官网](https://pypi.org/project/qmlease/) 下载.

完整的文档教程会在这个 wiki 中持续更新, 如需开始, 请阅读 [下一章节](installation.md)!

[^1]: 该版本号是从前身 lk-qtquick-scaffold 延续的. 更多细节请阅读后续章节.
