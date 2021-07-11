from time import time
from wasmtime import Store, Module, Instance

N = 1000_000_000

store = Store()
module = Module(store.engine, """
(module
    (func $sum_n (param i64) (result i64) (local i64)
       i64.const 0
       local.set 1            ;; res = 0
       (block
           (loop              ;; label B
               local.get 0    ;; n
               i64.eqz
               br_if 1        ;; if n == 0: goto A
               local.get 1
               local.get 0
               i64.add        ;; res + n
               local.set 1    ;; res = res + n
               local.get 0
               i64.const 1
               i64.sub        ;; n - 1
               local.set 0    ;; n = n - 1
               br 0           ;; goto B
           )
       )                      ;; label A
       local.get 1
    )
    (export "sum_n" (func $sum_n))
)
""")

instance = Instance(store, module, [])

f = instance.exports(store)["sum_n"]
for n in range(5):
    print(n, f(store, n), sum(range(n + 1)))

t0 = time()
print(f(store, N))
print("%9.3fs" % (time() - t0, ))

t0 = time()
print(sum(range(N + 1)))
print("%9.3fs" % (time() - t0, ))
