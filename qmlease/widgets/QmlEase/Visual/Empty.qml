import QtQuick
Item {
    Component.onCompleted: {
        if (this.width == 0) {
            this.width = 1
        }
        if (this.height == 0) {
            this.height = 1
        }
    }
}
