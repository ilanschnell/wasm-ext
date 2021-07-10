import ast, dis
from pprint import pprint


def disp_code(code):
    print('----- %s -----' % code.co_name)
    for name in dir(code):
        if name.startswith('co_'):
            print('%-20s  %s' % (name, code.__getattribute__(name)))

trans_op = {
    'BINARY_ADD': 'i32.add',
    'BINARY_MULTIPLY': 'i32.mul',
}

trans_cmp = {
    '<': 'i32.lt_u',
    '<=': 'i32.le_u',
    '==': 'i32.eq',
    '!=': 'i32.ne',
    '>': 'i32.gt_u',
    '>=': 'i32.ge_u',
}

fn = 't.py'

with open(fn) as fi:
    module_ast = ast.parse(fi.read())

#print(ast.dump(module_ast, indent=4, include_attributes=True))
code = compile(module_ast, fn, 'exec')
#dis.dis(code)

#disp_code(code)
functions = [c for c in code.co_consts if repr(c).startswith('<code object')]

wmod = ['(module']

for f in functions:
    disp_code(f)
    wmod.append('(func $%s' % f.co_name)
    if f.co_argcount:
        wmod.append('(param %s)' % ' '.join(f.co_argcount * ['i32']))
    wmod.append('(result i32)')
    if f.co_nlocals:
        wmod.append('(local %s)' % ' '.join(f.co_nlocals * ['i32']))
    for op in dis.get_instructions(f):
        if op.opname in trans_op:
            wmod.append(trans_op[op.opname])

        elif op.opname == 'LOAD_CONST':
            wmod.append('i32.const %d' % f.co_consts[op.arg])

        elif op.opname == 'LOAD_FAST':
            wmod.append('local.get %d' % op.arg)

        elif op.opname == 'STORE_FAST':
            wmod.append('local.set %d' % op.arg)

        elif op.opname == 'COMPARE_OP':
            cmp_op = dis.cmp_op[op.arg]
            wmod.append(trans_cmp[cmp_op])

        elif op.opname == 'POP_JUMP_IF_FALSE':
            wmod.append('br_if 0')

        print('    %-15s  %s' % (op.opname, op.arg))
    wmod.append(')')

for f in functions:
    wmod.append('(export "%s" (func $%s))' % (f.co_name, f.co_name))

wmod.append(')')

with open('u.wat', 'w') as fo:
    fo.write('\n'.join(wmod))

from wasmtime import Store, Module, Instance
store = Store()
module = Module.from_file(store.engine, 'u.wat')
instance = Instance(store, module, [])
foo = instance.exports(store)["foo"]
bar = instance.exports(store)["bar"]
add = instance.exports(store)["add"]
#mx_ = instance.exports(store)["max"]
print(foo(store))
print(bar(store, 5))
print(add(store, 2, 9))
#print(mx_(store, 2, 9))
