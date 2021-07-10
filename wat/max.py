from wasmtime import Store, Module, Instance

store = Store()
module = Module(store.engine, """
(module
    (func $max (param i32 i32) (result i32) (local i32)
        (block
            (block
                local.get 0
                local.get 1
                i32.gt_u
                br_if 0
                local.get 1
                local.set 0
                br 1
            )
        )
        local.get 0
    )
    (export "max" (func $max))
)
""")

instance = Instance(store, module, [])

m = instance.exports(store)["max"]
print(m(store, 3, 4))
print(m(store, 7, 2))
