from trans import t_file


py_file = 't.py'
wat_file = 'u.wat'

t_file(py_file, wat_file, debug=1)

import t

if 1:
    from wasmtime import Store, Module, Instance
    store = Store()
    module = Module.from_file(store.engine, wat_file)
    instance = Instance(store, module, [])
    foo = instance.exports(store)["foo"]
    bar = instance.exports(store)["bar"]
    add = instance.exports(store)["add"]
    sum7 = instance.exports(store)["sum7"]

    print(t.sum7(1000), sum7(store, 1000))
    print(t.bar(4), bar(store, 4))
    print(t.foo(), foo(store))

else:
    import loader
    import u

    print('---')
    print('sum7', id(u.sum7))
    print('bar', id(u.bar))
    print('foo', id(u.foo))

    print(t.sum7(1000), u.sum7(1000))
    print(t.bar(4), u.bar(4))
    print(t.foo(), u.foo())
