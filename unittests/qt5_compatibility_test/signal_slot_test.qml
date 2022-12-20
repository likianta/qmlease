// view.qml
import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    visible: true
    width: 400
    height: 300

    Text {
        anchors.centerIn: parent
        Component.onCompleted: {
            this.text = py.main.get_aaa()
            //                  ~~~~~~~~~
            py.main.aaa_changed.connect((new_text) => {
                //  ~~~~~~~~~~~          ~~~~~~~~
                this.text = new_text
            })

            py.main.bbb.connect((new_number) => {
                //  ~~~          ~~~~~~~~~~
                console.log('new number is ' + new_number)
            })

            console.log('start')
            py.main.simple_slot_method(100, 2)
            //                         ~~~~~~ 起始值和间隔值.
            console.log(
                py.main.complex_slot_method(
                    [1, 2, 3, 'a', 'b', 'c'],
                    {'d': 4, 'e': 5, 'f': 6},
                )
            )
        }
    }
}
