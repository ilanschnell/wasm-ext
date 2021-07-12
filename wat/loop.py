from time import time
from wasmtime import Store, Module, Instance

N = 1000 #1000_000_000



def sum7(n):
    if n < 1:
        return 0
    res = 0
    while n:
        res += n // 7
        n -= 1
    return res

store = Store()
module = Module(store.engine, """
(module
    (func $sum7 (param i64) (result i64)
       (local i64)
       (block
           (block
               local.get 0    ;; n
               i64.const 1
               i64.lt_s
               i32.eqz
               br_if 0        ;; if not n < 1: goto C
               i64.const 0
               return
               br 1
           )                  ;; label D
           ;; consequence
       )                      ;; label C

       i64.const 0
       local.set 1            ;; res = 0
       (block
           (loop              ;; label B
               local.get 0    ;; n
               i64.eqz
               br_if 1        ;; if n == 0: goto A
               local.get 1    ;; res
               local.get 0    ;; n
               i64.const 7
               i64.div_u
               i64.add
               local.set 1    ;; res = res + n / 7
               local.get 0    ;; n
               i64.const 1
               i64.sub
               local.set 0    ;; n = n - 1
               br 0           ;; goto B     (continue)
           )
       )                      ;; label A
       local.get 1
    )
    (export "sum7" (func $sum7))
)
""")

instance = Instance(store, module, [])

f = instance.exports(store)["sum7"]
for n in range(-10, 100):
    assert f(store, n) == sum7(n), 'n=%d  %r!=%r' % (n, f(store, n), sum7(n))

t0 = time()
print(f(store, N))
print("%9.3fs" % (time() - t0, ))

t0 = time()
print(sum7(N))
print("%9.3fs" % (time() - t0, ))
