from wasmtime import Store, Module, Instance


# max(a, b):
#     if a > b:
#         return a
#     a = b
#     return a

store = Store()
module = Module(store.engine, """
(module
    (func $max (param i32 i32) (result i32)
        (block
            local.get 0  ;; a
            local.get 1  ;; b
            i32.gt_u
            br_if 0      ;; if a > b: goto A
            local.get 1  ;; b
            local.set 0  ;; a = b
        )                ;; label A
        local.get 0      ;; a
    )
    (export "max" (func $max))
)
""")

instance = Instance(store, module, [])

m = instance.exports(store)["max"]
print(m(store, 3, 4))
print(m(store, 7, 2))
