from trans import t_file


py_file = 't.py'
wat_file = 'u.wat'

t_file(py_file, wat_file, debug=0)

if 0:
    from wasmtime import Store, Module, Instance
    store = Store()
    module = Module.from_file(store.engine, wat_file)
    instance = Instance(store, module, [])
    foo = instance.exports(store)["foo"]
    bar = instance.exports(store)["bar"]
    add = instance.exports(store)["add"]
    sum7 = instance.exports(store)["sum7"]
else:
    import loader
    import u

import t

#print(t.foo(), u.foo())
print(t.sum7(1000), u.sum7(1000))
