import qmlease as q
from random import randint


class Main(q.QObject):
    
    def __init__(self):
        super().__init__()
        self._model = q.Model(('name', 'age'))
        self._model.append_many([
            {'name': hex(randint(0, 0xffff)), 'age': randint(0, 100)}
            for _ in range(10)
        ])
        
    @q.Slot(object)
    def init_model(self, listview):
        listview['model'] = self._model
    
    @q.Slot()
    def change_some_item_name(self):
        i = randint(0, len(self._model) - 1)
        old_name = self._model[i]['name']
        self._model.update(i, {
            'name': (new_name := hex(randint(0, 0xffff))), 'age': randint(0, 100)
        })
        print('updated index {}: {} -> {}'.format(i, old_name, new_name), ':r2')


q.app.register(Main())
q.app.run('test/model_data_changed.qml')
