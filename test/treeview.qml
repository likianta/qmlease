import QtQuick
import QmlEase
import QmlEase.Composites

Window {
    TreeView {
//        anchors {
//            fill: parent
//            margins: 24
//        }
        anchors.centerIn: parent
        width: pysize.entry_width
        height: parent.height - 100
        model: [
            {
                'type': 'folder',
                'name': 'AAA',
                'path': 'BBB',
                'checked': false,
                'children_': [
                    {
                        'type': 'folder',
                        'name': 'CCC',
                        'path': 'DDD',
                        'checked': true,
                        'children_': [
                            {
                                'type': 'file',
                                'name': 'EEE',
                                'path': 'FFF',
                                'checked': false,
                            }
                        ]
                    },
                    {
                        'type': 'file',
                        'name': 'GGG',
                        'path': 'HHH',
                        'checked': false,
                    }
                ]
            }
        ]
    }
}
