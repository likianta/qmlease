import QtQuick 2.15
import LKWidgets 1.0
import dev.likianta.qmlease 1.0

LKWindow {
    MyObject {
        id: _myobj
        Component.onCompleted: {
            _myobj.test()
        }
    }
}
