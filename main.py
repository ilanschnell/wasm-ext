import ast, dis

import wasmtime.loader

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
    #wfun =
    for op in dis.get_instructions(f):
        if op.arg is None:
            s = ''
        if op.opname == 'LOAD_CONST':
            s = '%d (%r)' % (op.arg, f.co_consts[op.arg])
        elif op.opname == 'LOAD_FAST':
            s = '%d (%r)' % (op.arg, f.co_varnames[op.arg])
        else:
            s = ''
        print('    %-15s  %s' % (op.opname, s))

foo = wmod.add_function('foo', [i32], [i32])
foo.local.get(0)
foo.local.get(0)
foo.i32.add()
foo.block_end()
wmod.write_wasm('u')

import u
print(u.foo(7))
