from trans import t_file


py_file = 't.py'
wat_file = 'u.wat'

t_file(py_file, wat_file, debug=1)

from wasmtime import Store, Module, Instance
store = Store()
module = Module.from_file(store.engine, wat_file)
instance = Instance(store, module, [])
foo = instance.exports(store)["foo"]
bar = instance.exports(store)["bar"]
add = instance.exports(store)["add"]
sum7 = instance.exports(store)["sum7"]
print(foo(store))
print(bar(store, 5))
print(add(store, 2, 9))

from t import sum7 as sum7_py
for n in range(1000):
    assert sum7(store, n) == sum7_py(n), \
        'n=%d  %r!=%r' % (n, sum7(store, n), sum7_py(n))

print(sum7(store, 1000), sum7_py(1000))
