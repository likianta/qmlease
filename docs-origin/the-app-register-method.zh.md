# QmlEase `app.register` 使用详解

`app.register` 将 python class 或 instance 暴露到 qml 环境中.

目前支持以下暴露-调用方式:

1. 暴露 *实例* 到 *隐式* 命名空间

    python

    ```python
    from qmlease import QObject, app
    class MyObject(QObject): ...
    my_obj = MyObject()
    app.register(my_obj, name='my_obj', namespace='')
    #                         ~~~~~~~~            ~~
    #   注: 空字符串是缺省值.
    ```

    qml

    ```qml
    import QtQuick 2.15
    Item {
        Component.onCompleted: {
            py.my_obj.do_something()
        //  ~~~~~~~~~
        }
    }
    ```

2. 暴露 *实例* 到 *全局* 命名空间

    python

    ```python
    from qmlease import QObject, app
    class MyObject(QObject): ...
    my_obj = MyObject()
    app.register(my_obj, name='my_obj', namespace='global')
    #                         ~~~~~~~~            ~~~~~~~~
    #   注: 'global' 是特殊的关键词.
    ```

    qml

    ```qml
    import QtQuick 2.15
    Item {
        Component.onCompleted: {
            my_obj.do_something()
        //  ~~~~~~
        }
    }
    ```

3. 暴露 *实例* 到 *指定* 命名空间

    python

    ```python
    from qmlease import QObject, app
    class MyObject(QObject): ...
    my_obj = MyObject()
    app.register(my_obj, name='my_obj', namespace='my_space')
    #                         ~~~~~~~~            ~~~~~~~~~~
    ```

    qml

    ```qml
    import QtQuick 2.15
    Item {
        Component.onCompleted: {
            py.my_space.my_obj.do_something()
        //  ~~~~~~~~~~~~~~~~~~
        }
    }
    ```

4. 暴露 *类* 到 *隐式* 命名空间

    不支持此操作!

5. 暴露 *类* 到 *全局* 命名空间

    不支持此操作!

6. 暴露 *类* 到 *特定* 命名空间

    python

    ```python
    from qmlease import QObject, app
    class MyObject(QObject): ...
    app.register(MyObject, name='MyObject', namespace='MyLibrary')
    #                           ~~~~~~~~~~            ~~~~~~~~~~~
    #   注: 对于类, 建议使用 PascalCase 命名风格.
    ```

    qml

    ```qml
    import QtQuick 2.15
    import MyLibrary 1.0
    Item {
        MyObject {
            id: my_obj
        }
        Component.onCompleted: {
            my_obj.do_something()
        }
    }
    ```

## 参数详解

- 路径: `qmlease/application/register.py : class Register : def register`

- 定义:

    ```
    def register(
        self,
        qobj: QObject | type[QObject],
        name: str = '',
        namespace: str = '',
    ) -> None:
        ...
    ```

- 参数详解:

    - `qobj`

        要暴露到 qml 的对象, 可以是 `QObject` 的子类, 也可以是 `QObject` 的子类的实例.

    - `name`

        暴露到 qml 的对象的名称, 如果不指定, 则使用 `qobj` 的类名.

        此外注意, 如果 `qobj` 是类, 则名称会使用 PascalCase 风格, 也就是类名.

        如果 `qobj` 是实例, 则名称会使用 snake_case 风格, 也就是类名的小写形式.

    - `namespace`

        命名空间.

        如果 `qobj` 是实例, 则有以下选项:

        - 使用空字符串 (默认): 暴露到 `py` 命名空间中, 也就是 `py.my_obj`.
        - 使用 'global': 暴露到全局命名空间中, 也就是 `my_obj`.
        - 使用其他名称 (例如 'my_space'): 暴露到局部命名空间中, 也就是 `py.my_space.my_obj`.

        补充说明:

        - 使用 'global' 时, 建议以一个固定的单词作为开头, 例如 'py', 'my', 自己的品牌名缩写等.
        - 请避免使用 '.' 作为连接符, 推荐 snake_case 或 camelCase 形式.

        如果 `qobj` 是类, 则只能通过名称来暴露, 例如 `namespace='MyLibrary'`.

        补充说明:

        根据 qt 官方的文档示例, 命名空间的名称应该使用 `x.y.z` 风格, 也就是类似 'com.my_company.my_lib' 的形式.

        我们目前没有对此有严格要求, 在传入类时, 你可以使用 'MyLibrary' 和 'com.my_company.my_lib' 的任一风格.

## 疑问解答

### 为什么每种调用方式差异很大?

TODO

### 为什么不使用 QtQml 提供的 `qmlRegisterType`, `QmlElement` 等方法?

TODO

### 我的项目比较复杂, 注册的对象比较多 (可能分散在不同的模块), 怎么列出所有已注册的对象?

TODO

### 当出现重名, 特别是与内建的核心变量重名时, 会发生什么? 应该如何避免?

TODO

## 开发备忘

TODO

## 参考链接

- https://doc.qt.io/qtforpython/tutorials/qmlintegration/qmlintegration.html
- https://doc.qt.io/qtforpython/PySide6/QtQml/QmlNamedElement.html
- https://doc.qt.io/qtforpython/PySide6/QtQml/QmlSingleton.html
