import QtQuick
import QmlEase

Window {
    ListView {
        anchors {
            fill: parent
            margins: 12
        }
        model: [
            {name: 'AAA', age: 20},
            {name: 'BBB', age: 30},
            {name: 'CCC', age: 40},
        ]
        delegate: Text {
            text: (
                `index: ${model.index}; ` +
                `name: ${modelData.name}; ` +
                `age: ${modelData.age}`
            )
        }
//        delegate: Rectangle {
//            width: childrenRect.width
//            height: childrenRect.height
//            Text {
//                text: (
//                    `index: ${model.index}; ` +
//                    `name: ${modelData.name}; ` +
//                    `age: ${modelData.age}`
//                )
//            }
//        }
    }
}
