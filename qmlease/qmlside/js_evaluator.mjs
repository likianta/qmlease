// DELETE: this file has no usage.

export function evaluate(code) {
    return eval(code)
}

export function evaluate2(qobj, code, args) {
    return qobj.evaluate(code, args)
}

export function test_add(a, b) {
    console.log('a + b =', a + b)
    return a + b
}

export function test_echo(msg) {
    console.log(msg)
}
