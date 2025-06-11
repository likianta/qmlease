import QtQuick
import LKWidgets

Item {
    LKColumn {
        id: _col
        // width: 240
        Rectangle {
            id: _rect
            // width: pyenum.stretch
            color: 'yellow'
            LKText {
                id: _text
                text: 'hello world'
            }
        }
        LKButton {
            id: _btn
            text: 'Change text'
            onClicked: {
                _text.text = 'hello world - nihao shijie'
            }
        }
        LKButton {
            text: 'Check geometry'
            onClicked: {
                console.log(
                    _col.width,
                    _rect.width,
                    _text.width,
                    _btn.width,
                )
            }
        }
    }
    Component.onCompleted: {
        py.test_backend.handle(_rect)
    }
}
