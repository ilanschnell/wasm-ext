from wasmtime import Store, Module, Instance

store = Store()
module = Module(store.engine, """
(module
    (func $foo (result i32) (local i32 i32)
        i32.const 42
        local.set 0
        i32.const 7
        local.set 1
        local.get 0
        local.get 1
        i32.add
    )
    (export "foo" (func $foo))
)
""")
instance = Instance(store, module, [])

foo = instance.exports(store)["foo"]
print(foo(store))
