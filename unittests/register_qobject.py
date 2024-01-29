from qmlease import QObject
from qmlease import app


class A(QObject):
    pass


app.register(A(), 'AAA', 'PyAAA')
