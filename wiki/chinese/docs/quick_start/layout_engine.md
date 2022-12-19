# 布局引擎 (WIP)

```qml
// some_view.qml
import QtQuick

Column {
    height: 100
    
    Item { id: item1; height: 20  }
    Item { id: item2; height: 0.4 }
    Item { id: item3; height: 0   }
    Item { id: item4; height: 0   }

    Component.onCompleted: {
        // horizontally center children
        pylayout.auto_align(this, 'hcenter')

        // auto size children:
        //  width > 1: as pixels
        //  width > 0 and < 1: as percent of left spared space
        //  width = 0: as stretch to fill the left spared space
        pylayout.auto_size_children(this, 'vertical')
        //  the result is:
        //      item1: 20px
        //      item2: (100 - 20) * 0.4 = 32px
        //      item3: (100 - 20 - 32) * 0.5 = 24px
        //      item4: (100 - 20 - 32) * 0.5 = 24px
        //          (item 3 and 4 share the left space equally.)
    }
}
```
