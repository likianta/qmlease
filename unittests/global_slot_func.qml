import QtQuick
import LKWidgets

LKWindow {
    color: find_color('black_5')
//    color: foo2.find_color('black_5')

    Component.onCompleted: {
        console.log(foo1)
        console.log(foo2)
        console.log(foo2.find_color)
        console.log(foo2.find_color('blue_5'))
        console.log(find_color)
        console.log(find_color('blue_5'))
    }
}
