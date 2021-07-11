from wasmtime import Store, Module, Instance


N = 10_000

store = Store()
module = Module.from_file(store.engine, './collatz.wat')

instance = Instance(store, module, [])

f = instance.exports(store)["collatz"]
m = 0
for i in range(1, N):
    j = f(store, i)
    if j > m:
        m = j
        print("%3d: %9d" % (m, i))
