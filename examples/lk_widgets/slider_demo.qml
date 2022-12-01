import LKWidgets 1.0

LKWindow {
    id: root
    width: 400
    height: 600

    LKColumn {
        anchors.fill: parent
        anchors.margins: 24
        alignment: 'hcenter,hfill'
        autoSize: true

        LKSlider {
            height: 0
            showText: false
        }

        LKSlider {
            height: 0
            showText: true
        }

        LKSlider {
            height: 0
            model: {0.0: 'low', 0.5: 'medium', 1.0: 'high'}
            showText: false
        }

        LKSlider {
            height: 0
            model: {0.0: 'low', 0.5: 'medium', 1.0: 'high'}
            showText: true
        }
    }
}
