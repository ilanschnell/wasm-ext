import ast
import inspect

import trans


fn = 't.py'

with open(fn) as fi:
    module_ast = ast.parse(fi.read())

#print(ast.dump(module_ast, indent=4, include_attributes=True))
code = compile(module_ast, fn, 'exec')
#dis.dis(code)

functions = [c for c in code.co_consts if inspect.iscode(c)]

wmod = ['(module']
for f in functions:
    trans.t_function(f, wmod, debug=1)
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
sum7 = instance.exports(store)["sum7"]
print(foo(store))
print(bar(store, 5))
print(add(store, 2, 9))
print(sum7(store, 1000_000_000))
