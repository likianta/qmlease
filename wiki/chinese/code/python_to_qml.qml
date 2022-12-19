// view.qml
import QtQuick

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
            py.main.ccc(100, 2)
            //          ~~~~~~ 起始值和间隔值.
        }
    }
}