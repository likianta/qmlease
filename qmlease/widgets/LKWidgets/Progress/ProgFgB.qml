import QtQuick 2.15
import ".."

Item {
    id: root
    width: pysize.progress_width
    height: pysize.progress_height

    property string color: pycolor.progress_fg
    property int    radius: pysize.radius_s
    property int    step: 0
    property int    totalSteps: 0  // FIXME: must >= 2?
    property real   __stepSize: width / (__totalSteps - 1)
    property int    __totalSteps: totalSteps >= 2 ? totalSteps : 2

    signal clicked(int step)

    Rectangle {
        id: _prog
        width: root.__stepSize * root.step
        height: parent.height
        radius: root.radius
        color: root.color
    }

    Row {
        id: _dotted
        anchors.fill: parent
        spacing: width / (root.__totalSteps - 1)

        Repeater {
            anchors.fill: parent
            model: root.totalSteps
            delegate: Item {
                anchors.verticalCenter: parent.verticalCenter
                width: 1
                height: 1

                LKCircle {
                    id: _dot
                    anchors.centerIn: parent

                    property int  index: model.index
                    property bool selected: index <= root.step

                    LKMouseArea {
                        id: _dot_area
                        anchors.fill: parent
                        onClicked: root.clicked(_dot.index)
                    }

                    Component.onCompleted: {
                        this.radius = Qt.binding(() => {
                            if (this.selected) {
                                return pysize.dot_radius_active
                            } else {
                                return pysize.dot_radius_default
                            }
                        })
                        this.color = Qt.binding(() => {
                            if (this.selected) {
                                return pycolor.dot_active
                            } else if (_dot_area.hovered) {
                                return pycolor.dot_hovered
                            } else {
                                return pycolor.dot_default
                            }
                        })
                        this.border.width = Qt.binding(() => {
                            if (this.selected) {
                                return pysize.dot_border_active
                            } else if (_dot_area.hovered) {
                                return pysize.dot_border_hovered
                            } else {
                                return pysize.dot_border_default
                            }
                        })
                        this.border.color = Qt.binding(() => {
                            if (this.selected) {
                                return pycolor.dot_border_active
                            } else if (_dot_area.hovered) {
                                return pycolor.dot_border_hovered
                            } else {
                                return pycolor.dot_border_default
                            }
                        })
                    }
                }
            }
        }
    }
}
