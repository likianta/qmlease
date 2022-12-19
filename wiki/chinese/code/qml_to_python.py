from lk_utils import xpath
from qmlease import QObject, app, slot


class Main(QObject):
    @slot(object)
    def set_text_view(self, text_item: QObject) -> None:
        """
        如果 text_item 宽度大于 100px, 则显示 A 文字; 否则显示 B 文字.
        """
        if text_item['width'] > 100:
            text_item['text'] = 'This is a long description.'
        else:
            text_item['text'] = 'Short desc'


app.register(Main(), 'main')
app.run(xpath('text_in_variable_width.qml'))
