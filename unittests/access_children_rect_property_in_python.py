from functools import partial
from lk_utils import p
from qmlease import QObject, app, bind_prop, slot


class TestBackend(QObject):
    @slot(object)
    def handle(self, item):
        bind_prop(
            item, 'width', 'childrenRect',
            custom_handler=partial(self._sync_size_to_children_rect, item),
            # effect_now=True
        )
        self._sync_size_to_children_rect(item, item['childrenRect'])

    @staticmethod
    def _sync_size_to_children_rect(item, rect) -> None:
        item['width'] = rect.width()
        item['height'] = rect.height()
        print(item['width'], item['height'], ':vit')


app.register(TestBackend())
app.run(p('access_children_rect_property_in_python.qml'), debug=True)
