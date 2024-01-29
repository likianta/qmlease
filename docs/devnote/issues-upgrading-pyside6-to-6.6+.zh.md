# 将依赖库 PySide6 从 6.4 升级到 6.6 后遇到的问题和修复备忘

## Mixin 报错

这是之前 (pyside6 6.4) 可以工作的代码:

```python
from qmlease import QObject

class AAA:
    def __init__(self):
        print(self.aaa)
        
class BBB(QObject, AAA):
    def __init__(self):
        QObject.__init__(self)
        self.aaa = 111
        AAA.__init__(self)

BBB()
```

现在的报错出现在, 当 BBB 实例化时, 其父类 AAA 的初始化方法被触发了, 导致 `self.aaa = 111` 还没有被执行, 就执行了 `print(self.aaa)`. 于是产生了 `AttributeError: 'BBB' object has no attribute 'aaa'`.

目前, 我们的解决方法是不使用 mixin, 改为单继承体系. 这是一个不完美的解决方案:

```python
from qmlease import QObject

class AAA(QObject):
    def __init__(self):
        super().__init__()
        print(self.aaa)
        
class BBB(AAA):
    def __init__(self):
        super().__init__()
        self.aaa = 111

BBB()
```

## Basic Style 警告

...
