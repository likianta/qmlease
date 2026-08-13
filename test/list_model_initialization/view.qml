import QtQuick
import QtQuick.Window

Window {
    visible: true
    width: 800
    height: 600
    
    ListView {
        anchors.fill: parent
        anchors.margins: 20
        // model: sidebar.init_model()
        delegate: Text {
            text: `text: ${model.text}, icon: ${model.icon}`
        }
        Component.onCompleted: {
            this.model = sidebar.init_model()
            // sidebar.init_model_2(this)
        }
    }
}