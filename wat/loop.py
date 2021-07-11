from time import time
from wasmtime import Store, Module, Instance

N = 100_000_000

store = Store()
module = Module(store.engine, """
(module
    (func $sum_n (param i64) (result i64) (local i64)
       i64.const 0
       local.set 1
       (block
           local.get 0
           i64.const 1
           i64.le_u
           br_if 0
           (loop
               local.get 1
               local.get 0
               i64.add
               local.set 1
               local.get 0
               i64.const -1
               i64.add
               local.tee 0
               i64.eqz
               br_if 1
               br 0
           )
       )
       local.get 1
    )
    (export "sum_n" (func $sum_n))
)
""")

instance = Instance(store, module, [])

f = instance.exports(store)["sum_n"]
for n in range(5):
    print(n, f(store, n), sum(range(n)))

t0 = time()
print(f(store, N))
print("%9.6f" % (time() - t0, ))

t0 = time()
print(sum(range(N)))
print("%9.6f" % (time() - t0, ))
