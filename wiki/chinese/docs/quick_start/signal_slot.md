# 更加自然的信号与槽写法

相比于官方库中的信号与槽, qmlease 对它们做了简答的封装, 带来了以下特性:

- 使用小写的名称: `signal` `slot`
- ide 能够正确地识别类型标注, 并提供自动补全:

    ![](../images/20221219174653.png)

    与官方的对比:

    ![](../images/20221219175054.png)

- 参数可以用原生的 python 类型表示 (qmlease 会自动完成类型转换)

    ![](../images/20221219174909.png)

- 非侵入式的设计: 被 slot 装饰的函数, 仍然可以像往常一样被调用

## 自动转换类型 (清单)

下面是完整的可自动转换的类型清单:

`slot(*args)`

| Alias         | Real value    | Note              |
| ------------- | ------------- |------------------ |
| `bool`        | `bool`        | basic type        |
| `float`       | `float`       | basic type        |
| `int`         | `int`         | basic type        |
| `str`         | `str`         | basic type        |
| `QObject`     | `QObject`     | object            |
| `object`      | `QObject`     | object            |
| `'item'`      | `QObject`     | object (string)   |
| `'object'`    | `QObject`     | object (string)   |
| `'qobject'`   | `QObject`     | object (string)   |
| `dict`        | `QJSValue`    | qjsvalue          |
| `list`        | `QJSValue`    | qjsvalue          |
| `set`         | `QJSValue`    | qjsvalue          |
| `tuple`       | `QJSValue`    | qjsvalue          |
| `...`         | `QJSValue`    | qjsvalue          |
| `'any'`       | `QJSValue`    | qjsvalue (string) |

`slot(result=...)`

| Alias     | Real value    | Note          |
| --------- | ------------- |-------------- |
| `None`    | `None`        | basic type    |
| `bool`    | `bool`        | basic type    |
| `float`   | `float`       | basic type    |
| `int`     | `int`         | basic type    |
| `str`     | `str`         | basic type    |
| `dict`    | `'QVariant'`  | qvariant      |
| `list`    | `'QVariant'`  | qvariant      |
| `set`     | `'QVariant'`  | qvariant      |
| `tuple`   | `'QVariant'`  | qvariant      |
| `...`     | `'QVariant'`  | qvariant      |

## 非侵入式设计 (示例)

```python
from qmlease import QObject, slot

class MyObject(QObject):
    @slot(int, str, result=list)
    def foo(self, index, name):
        return [index, name]

my_obj = MyObject()
# 你可以像普通的实例方法那样去调用 `foo` (仿佛 slot 不存在一样).
my_obj.foo(1, 'hello')  # -> [1, 'hello']
```
