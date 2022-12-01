import QtQuick 2.15
import QtQuick.Dialogs 1.3
import "./LCButtons"
import "./LCStyle/dimension.js" as LCDimension

LCTextField {
    id: root
    p_title: 'Select path:'

    property alias  p_borderless: _btn.p_borderless
    property alias  p_dialogTitle: _dialog.title
    property alias  p_filetype: _dialog.nameFilters  // [str, ...]
    /*      Examples:
                ["All files (*.*)"]
                ["Excel file (*.xlsx *.xls)"]
                ["PDF file (*.pdf)"]
                ["Plain file (*.txt *.md *.rst *.json *.ini)"]
                ["Text file (*.txt)", "All files (*.*)"]
     */
    property alias  p_path: root.p_value
    property alias  p_selectFolder: _dialog.selectFolder
    property alias  p_selectMultiple: _dialog.selectMultiple
    // inherits:
    //      p_alignment
    //      p_hint
    //      p_title
    //      p_value

    LCButton {
        id: _btn
        anchors {
            right: parent.right
            verticalCenter: parent.verticalCenter
        }
        p_text: "Browse"

        onClicked: _dialog.open()

        FileDialog {
            id: _dialog
            // 注意: QML 会报一个错误: 'QML TableViewColumn: Accessible must be
            //       attached to an Item'. 这个错误似乎在 Windows 系统上出现, 是
            //       由 QML 的内部组件 TableViewColumn 引起的, 您可以选择忽略它.
            // folder: shortcuts.desktop
            selectExisting: true
            selectFolder: false
            selectMultiple: false
            title: "Dialog"

            onAccepted: {
                /*
                    Note that `this.fileUrl` is typeof Object, not string. We
                    should convert it to string before we assign it to `p_path`.
                    Use `fileUrl + ""` to convert it to string, the value is
                    like 'file:///d:/...', slice out 'file:///' then pass it to
                    `p_path`.
                 */
                let path = this.fileUrl + ""
                if (path.length < 8) {
                    root.p_path = path  // usually this means the `path` is an
                    //  empty string (it happended maybe because user stayed
                    //  long time at dialog pane, i'm not much sure about this).
                } else {
                    root.p_path = path.slice(8)
                    //  e.g. 'file:///D:/A/B/C.txt' -> 'D:/A/B/C.txt'
                }
            }
        }
    }

    Component.onCompleted: {
        root.children[1].anchors.right = _btn.left
        root.children[1].anchors.rightMargin = LCDimension.HSpacingM
    }
}
