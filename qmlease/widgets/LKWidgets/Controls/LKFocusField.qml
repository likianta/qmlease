import QtQuick 2.15

FocusScope {
    focus: true
    Keys.onPressed: (evt) => {
        lkscope.on_key(evt.key, evt.modifiers)
    }
}
