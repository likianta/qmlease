# How to import LKWidgets

In your .qml file:

```qml
import LKWidgets 1.0

LKWindow {

    LKRectangle {
        anchors.fill: parent
        anchors.margins: 32

        LKText {
            anchors.centerIn: parent
            text: 'hello world'
        }
    }
}
```

When `import LKWidgets 1.0`, you can use all widgets that are listed in './qmldir'.

Import submodules:

```qml
import LKWidgets 1.0
import LKWidgets.Buttons 1.0
import LKWidgets.Panels 1.0

LKWindow {
    color: '...'

    LKSidebar {
        // this comes from `LKWidgets.Panels`
        id: _sidebar
        anchors {
            left: parent.left
            top: parent.top
            bottom: parent.bottom
            margins: 12
        }
        width: 120
        model: [
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
        ]
    }

    LKRectangle {
        // this comes from `LKWidgets`
        id: _rect
        anchors {
            left: _sidebar.right
            top: parent.top
            bottom: parent.bottom
            right: parent.right
            margins: 12
        }
        color: '...'

        LKButton {
            // this comes from `LKWidgets.Buttons`
            anchors.centerIn: parent
            text: 'click me'
        }
    }
}
```

BTW to quick access most frequently used widgets from submodules, I've also exposed some of them into main module -- `LKWidgets`. It means you can use `LKButton` after `import LKWidgets 1.0`, it points to the same widget as `import LKWidgets.Buttons 1.0` does.

For more information, just check each module's "qmldir" file.
