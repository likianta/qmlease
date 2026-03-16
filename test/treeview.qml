import QtQuick
import QmlEase
import QmlEase.Composites

Window {
    TreeView {
        anchors {
            fill: parent
            margins: 24
        }
        checkable: true
        model: [
            {
                'type': 'folder',
                'name': 'AAA',
                'path': 'BBB',
                'checked': false,
                'children': [
                    {
                        'type': 'folder',
                        'name': 'CCC',
                        'path': 'DDD',
                        'checked': true,
                        'children': [
                            {
                                'type': 'folder',
                                'name': 'EEE',
                                'path': 'FFF',
                                'checked': false,
                                'children': [
                                    {
                                        'type': 'file',
                                        'name': 'GGG',
                                        'path': 'HHH',
                                        'checked': false,
                                    },
                                    {
                                        'type': 'file',
                                        'name': 'III',
                                        'path': 'JJJ',
                                        'checked': false,
                                    },
                                ]
                            }
                        ]
                    },
                    {
                        'type': 'file',
                        'name': 'KKK',
                        'path': 'LLL',
                        'checked': false,
                    }
                ]
            }
        ]
    }
}
