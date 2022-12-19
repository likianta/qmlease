# main.py
# 以下展示了信号, 属性, 槽函数的使用.
from time import sleep
from lk_utils import new_thread, xpath
from qmlease import AutoProp, QObject, app, signal, slot

class Main(QObject):
    aaa = AutoProp('You got AAA (0)')
    #   在 python 端, 你可以认为 aaa 是一个字符串, 并完全按照字符串对待它.
    #   在 qml 端, 使用 `get_aaa()` `set_aaa(...)` 进行读和写.
    #   同时, aaa 还自动生成了 `aaa_changed` 信号 (通过 qmlease 的魔术方法).
    bbb = signal(int)

    @slot(int, int)
    def ccc(self, offset: int, interval: int) -> None:

        @new_thread()
        def auto_update():
            for i in range(offset, offset + 100, interval):
                print(i)
                self.bbb.emit(i)
                self.aaa = f'You got AAA ({i})'
                #   当我们变更了 aaa 的值, 它会自动产生 `aaa_changed.emit('You got AAA ...')` 信号.
                sleep(0.5)

        auto_update()

app.register(Main(), 'main')  # 注意第一个参数是类的实例.
app.run(xpath('python_to_qml.qml'))