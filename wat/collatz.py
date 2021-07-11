from wasmtime import Store, Module, Instance


N = 10_000

store = Store()
module = Module(store.engine, """
(module
    (func $collatz (param $n i64) (result i64)
       (local i64)
       i64.const 0
       local.set 1                    ;; j = 0   (result)
       (block
           (loop                      ;; label B
               local.get $n           ;; n
               i64.const 1
               i64.eq
               br_if 1                ;; if n == 1: goto A
               (block
                   (block
                       local.get $n
                       i64.const 2
                       i64.rem_u      ;; n % 2
                       i32.wrap_i64
                       br_if 0        ;; if n % 2: goto D
                       local.get $n
                       i64.const 2
                       i64.div_u
                       local.set $n   ;; n = n / 2
                       br 1           ;; goto C
                   )                  ;; label D
                   i64.const 3
                   local.get $n
                   i64.mul
                   i64.const 1
                   i64.add
                   local.set $n       ;; n = 3 * n + 1
               )                      ;; label C
               local.get 1
               i64.const 1
               i64.add
               local.set 1            ;; j = j + 1
               br 0                   ;; goto B     (continue)
           )
       )                              ;; label A
       local.get 1
    )
    (export "collatz" (func $collatz))
)
""")

instance = Instance(store, module, [])

f = instance.exports(store)["collatz"]
m = 0
for i in range(1, N):
    j = f(store, i)
    if j > m:
        m = j
        print("%3d: %9d" % (m, i))
