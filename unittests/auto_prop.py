from typing import cast

from lk_utils import xpath

from qmlease import AutoProp
from qmlease import Model
from qmlease import QObject
from qmlease import app
from qmlease import slot


class MyObject(QObject):
    width = AutoProp(100)
    model = cast(Model, AutoProp(Model(('name', 'age')), object))
    
    def __init__(self):
        super().__init__()
        self.model.append_many([
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 20},
        ])
    
    @slot()
    def test_update(self):
        print(self.width)
        print(self.model)
        self.width = 200
        self.model.append({'name': 'Cindy', 'age': 22})


app.register(MyObject(), 'myobj')
app.run(xpath('auto_prop.qml'))
