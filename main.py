import ast, dis
from pprint import pprint

from wasm_encoder import Module, i32


def disp_code(code):
    print('----- %s -----' % code.co_name)
    for name in dir(code):
        if name.startswith('co_'):
            print('%-20s  %s' % (name, code.__getattribute__(name)))


fn = 't.py'

with open(fn) as fi:
    module_ast = ast.parse(fi.read())

#print(ast.dump(module_ast, indent=4, include_attributes=True))
code = compile(module_ast, fn, 'exec')
#dis.dis(code)

#disp_code(code)
functions = [c for c in code.co_consts if repr(c).startswith('<code object')]

wmod = Module()

for f in functions:
    disp_code(f)
    wfun = wmod.add_function(f.co_name, f.co_argcount * [i32], [i32])
    for op in dis.get_instructions(f):
        if op.opname == 'LOAD_CONST':
            wfun.i32.const(f.co_consts[op.arg])

        elif op.opname == 'LOAD_FAST':
            wfun.local.get(op.arg)

        elif op.opname == 'STORE_FAST':
            wfun.local.set(op.arg)

        elif op.opname == 'BINARY_ADD':
            wfun.i32.add()

        elif op.opname == 'BINARY_MULTIPLY':
            wfun.i32.mul()

        print('    %-15s  %s' % (op.opname, op.arg))
    wfun.block_end()


wmod.write_wasm('u')

from wasmtime import Store, Module, Instance
store = Store()
module = Module.from_file(store.engine, 'u.wasm')
instance = Instance(store, module, [])
foo = instance.exports(store)["foo"]
bar = instance.exports(store)["bar"]
add = instance.exports(store)["add"]
print(foo(store))
print(bar(store, 5))
print(add(store, 2, 9))
