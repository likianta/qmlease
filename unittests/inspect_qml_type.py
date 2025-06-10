import remote_ipython
from lk_utils import run_new_thread
from qmlease import QObject, app, slot


class Inspector(QObject):
    @slot(object)
    def inspect(self, item: QObject) -> None:
        run_new_thread(
            remote_ipython.run_server,
            ({'item': item},),
        )
        # remote_ipython.run_server({'parent': parent})
        # for child in parent.children():
        #     print(child)
        #     remote_ipython.run_server({'child': child})


app.register(Inspector(), 'inspector')
app.run('unittests/inspect_qml_type.qml', debug=True)
# pox unittests/inspect_qml_type.py
