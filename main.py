import ast, dis

from wasmtime import Store, Module, Instance

from wasm_encoder import Module as DB_Module, i32


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

disp_code(code)
disp_code(code.co_consts[0])

dis.dis(code)
codes = [code, code.co_consts[0]]

mod = DB_Module()

for code in codes:
    print(code)
    print(code.co_names)
    for op in dis.get_instructions(code):
        if op.arg is None:
            s = ''
        if op.opname == 'LOAD_CONST':
            s = '%d (%r)' % (op.arg, code.co_consts[op.arg])
        elif op.opname == 'LOAD_FAST':
            s = '%d (%r)' % (op.arg, code.co_varnames[op.arg])
        else:
            s = ''
        print('    %-15s  %s' % (op.opname, s))

foo = mod.add_function('foo', [i32], [i32])
foo.local.get(0)
foo.local.get(0)
foo.i32.add()
foo.block_end()
mod.write_wasm('t')

store = Store()
module = Module.from_file(store.engine, 't.wasm')
instance = Instance(store, module, [])
myfoo = instance.exports(store)["foo"]
print(myfoo(store, 7))

