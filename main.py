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

w_mod = ["""(module
(func $unary_negative (param i64) (result i64)
i64.const 0 local.get 0 i64.sub)"""]
for f in functions:
    trans.t_function(f, w_mod, debug=0)
for f in functions:
    w_mod.append('(export "%s" (func $%s))' % (f.co_name, f.co_name))
w_mod.append(') ;; module\n')

with open('u.wat', 'w') as fo:
    fo.write('\n'.join(w_mod))

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

from t import sum7 as sum7_py
for n in range(1000):
    assert sum7(store, n) == sum7_py(n), \
        'n=%d  %r!=%r' % (n, sum7(store, n), sum7_py(n))

print(sum7(store, 1000), sum7_py(1000))
