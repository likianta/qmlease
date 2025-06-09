import QtQuick
import LKWidgets

LKWindow {
    width: 400
    height: 300
    color: 'yellow'
    Component.onCompleted: {
        console.log('window opened')
    }
}
