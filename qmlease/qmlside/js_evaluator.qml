import QtQml 2.0

QtObject {
    function evaluate(code, args, console) {
//        console.log('evaluating code', code, args)
        // return eval(`(() => {${code}})()`)
        return eval(code)
    }

    function createCustomLogger(file_id) {
        return {'log': (...args) => console.log(file_id, ...args)}
    }

    function useDefaultLogger() {
        return console
    }

    function getQtBinding() {
        return {'binding': Qt.binding}
    }

    function bindAnchors(a, b) {
        // pass
    }
}
