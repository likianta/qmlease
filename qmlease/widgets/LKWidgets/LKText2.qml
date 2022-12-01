// https://stackoverflow.com/questions/1337523/measuring-text-width-in-qt
import QtQuick 2.15

LKText {
    id: root

    property string maxText
    property int    maxWidth: measureContent(root.text)

    onMaxTextChanged: {
        this.maxWidth = measureContent(this.maxText)
    }

    function measureContent(text) {
//        if (text == '') {
//            text = root.text
//        }
        if (text.includes('\n')) {
            text = pyside.eval(`
                return max(text.splitlines(), key=len)
            `, {'text': text})
        }
        return _metrics.advanceWidth(text) * 1.2
    }

    FontMetrics {
        id: _metrics
        font: root.font
    }
}
