import qmlease as qe

class Main(qe.QObject):
    @qe.Slot(object, str)
    def inspect(self, listview, remark):
        # print(remark, listview['model'], listview['count'], ':i4l')
        print(
            remark, 
            # listview.qobj.model if listview.qobj.property('model') is None else
            # listview.qobj.property('model'), 
            listview.qobj.property('model'),
            listview['count'], 
            ':i4l'
        )

    @qe.Slot(object)
    def create_model_in_pyside(self, listview):
        print(listview['model'])
        listview['model'] = qe.ListModel.from_list((
            {'name':  'AAA', 'number': 111},
            {'name':  'BBB', 'number': 222},
        ))
        print(listview['model'])

qe.app.register(Main())
qe.app.run('test/model_accessibility_in_pyside.qml')
