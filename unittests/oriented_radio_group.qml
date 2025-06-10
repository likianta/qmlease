import QtQuick
import LKWidgets
import LKWidgets.Controls

LKColumn {
    width: 800
    height: 800
    // autoSize: true
    LKRadioGroup {
        id: horizontalGroup
        width: pyenum.stretch
        title: 'AAA'
        model: ['BBB', 'CCC', 'DDD']
        horizontal: true
        Component.onCompleted: {
            console.log(this.width, this.height)
        }
    }
    LKRadioGroup {
        id: verticalGroup
        height: pyenum.stretch
        title: 'EEE'
        model: ['FFF', 'GGG', 'HHH']
        horizontal: false
        Component.onCompleted: {
            console.log(this.width, this.height)
        }
    }
    Component.onCompleted: {
        console.log(
            [this.width, this.height],
            [horizontalGroup.width, horizontalGroup.height],
            [verticalGroup.width, verticalGroup.height],
        )
    }
}
