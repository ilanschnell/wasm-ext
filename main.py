from time import time

from trans import t_file


py_file = 'demo.py'
wat_file = 'u.wat'

t_file(py_file, wat_file, debug=0)

import demo
import loader
import u

for i in range(0, 100):
    assert demo.foo(i) == u.foo(i)

t0 = time()
print(u.foo(1000_000_000))
print('%.3f sec' % (time() - t0))
