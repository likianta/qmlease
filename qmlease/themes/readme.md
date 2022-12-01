## How to use lk-qtquick-scaffold preset themes

In qml file:

```qml
import QtQuick
import Theme.SimpleUI
// You can also import other themes like:
//      import Theme.LightClean
//      import Theme.Whitey
//      ...

// `SWindow` is a component from Theme.SimpleUI. 
// You can find all available components in './Theme/SimpleUI/qmldir' file.
SWindow {
    id: win
    width: 600
    height: 400
    
    // `HBox` and `VBox` also come from Theme.SimpleUI. They are something like 
    // Row and Column but more intelligent.
    HBox {
        VBox {
            id: left_column
            // ...
        }
        VBox {
            id: right_column
            // ...
        }
    }
}
```
