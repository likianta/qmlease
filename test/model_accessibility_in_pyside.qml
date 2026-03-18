import QtQuick
import QtQuick.Layouts
import QmlEase

Window {
    
    ColumnLayout {
        anchors {
            // fill: parent
            horizontalCenter: parent.horizontalCenter
            top: parent.top
            bottom: parent.bottom
            margins: 24
        }
        width: 240

        ListView {
            id: _lv1
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: 3
            delegate: Text { text: `No.${modelData}` }
        }

        ListView {
            id: _lv2
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: [
                { 'name': 'AAA', 'number': 111 },
                { 'name': 'BBB', 'number': 222 },
            ]
            delegate: Text { 
                text: `Name: ${modelData.name}; Number: ${modelData.number}` 
            }
        }

        ListView {
            id: _lv3
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: ListModel {
                ListElement {
                    name: 'AAA'
                    number: 111
                }
                ListElement {
                    name: 'BBB'
                    number: 222
                }
            }
            delegate: Text { 
                text: `Name: ${model.name}; Number: ${model.number}` 
            }
        }

        ListView {
            id: _lv4
            Layout.fillWidth: true
            Layout.fillHeight: true
            delegate: Text { 
                text: `Name: ${model.name}; Number: ${model.number}` 
            }
            Component.onCompleted: {
                py.main.create_model_in_pyside(this)
            }
        }

        ListView {
            id: _lv5
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: []
            delegate: Text { 
                text: `Name: ${model.name}; Number: ${model.number}` 
            }
            Component.onCompleted: {
                py.main.create_model_in_pyside(this)
            }
        }

        ListView {
            id: _lv6
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: ListModel {
                ListElement {
                    name: 'AAA'
                    number: 111
                }
                ListElement {
                    name: 'BBB'
                    number: 222
                }
            }
            delegate: Text { 
                text: `Name: ${model.name}; Number: ${model.number}` 
            }
            Component.onCompleted: {
                py.main.inspect(this, 'pymodel3 (before)')
                py.main.create_model_in_pyside(this)
            }
        }

        Button {
            Layout.fillWidth: true
            text: 'Test'
            onClicked: {
                py.main.inspect(_lv1, 'integer model')
                py.main.inspect(_lv2, 'js array')
                py.main.inspect(_lv3, 'listmodel object')
                py.main.inspect(_lv4, 'pymodel1')
                py.main.inspect(_lv5, 'pymodel2')
                py.main.inspect(_lv6, 'pymodel3 (after)')
            }
        }
    }
}
