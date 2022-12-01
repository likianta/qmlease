import QtQuick 2.15
import QtQuick.Dialogs 1.3

FileDialog {
    // https://doc.qt.io/qt-6/qml-qtquick-dialogs-filedialog.html
    // https://doc.qt.io/qt-6/qml-qtquick-dialogs-dialog.html

    signal selected(string path)

    onAccepted: {
        console.log(this.fileUrl)
        //  e.g. 'file:///Users/xxx/Documents/firware-1.0.0.bin'
        // note `this.selectedFile` type is not regular string.
        const path = pyside.eval(`
            import os
            if os.name == 'nt':
                return url[8:]
            else:
                return url[7:]
        `, {'url': this.fileUrl + ''})
        this.selected(path)
    }
}
