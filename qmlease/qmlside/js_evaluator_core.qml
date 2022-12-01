import QtQuick 2.15

Item {
    id: root
    objectName: 'JsEvaluator'

    function bind(t_obj, s_obj, expression) {
        eval(expression)
    }

    function connect_func(s_obj, s_prop, func_id, participants) {
        eval(`
            s_obj.${s_prop} = Qt.binding(
                () => PySide.eval('${func_id}', ${participants})
            )
        `)
    }

    function create_component(qmlfile) {
        return Qt.createComponent(qmlfile)
    }

    function create_object(component, container) {
        return component.createObject(container)
    }

    function eval_js(code, args) {
        return eval(code)
    }

    function test() {
        return 'JsEvaluator is ready to use'
    }

    // ------------------------------------------------------------------------

    function get_content_width(text, pixel_size) {
        _text.font.pixelSize = pixel_size
        _text.text = text
        return _text.contentWidth
    }

    Text {
        id: _text
        font.pixelSize: 12
    }
}
