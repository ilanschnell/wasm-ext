from time import time

from trans import t_file


py_file = 'demo.py'
wat_file = 'u.wat'

t_file(py_file, wat_file, debug=0)

import loader
import u

t0 = time()
result = u.foo(1000_000_000)
print('%d    %.3f sec' % (result, time() - t0))
