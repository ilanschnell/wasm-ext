Web-Assembly extensions for Python
==================================

We would like to present the possibility to create Python extensions
in Web-Assembly written in Python.  In this work in experimental, we
explore interesting opportunities.  We have created a small Python to
Web-Assembly compiler, which allows compiling a very limited subset of
Python to Web-Assembly, and then import these directly into Python.
Although Web-Assembly was created primarily for the web, as a way to
execute machine code in the browser, it has become a standard for
portable machine code which can be executed on any system.  The advantage
of Web-Assembly over other portable machine code formats (such as LLVM-IR)
are:
  * it is well documented and very stable
  * the binary `.wasm` format is very compact (because it was designed to be
    loaded into the browser over the internet)
  * the textual equivalent format `.wat`
  * there are a several implementations of the runtime, namely `wasmer` and
    `bytecode-alliance` for many systems, as well as browser support

In the process of studying Web-Assembly, I realized its striking similarity
to Python Bytecode, as both are executed on a stack machine.  This has lead
me to write an "opcode transpiler".  So the compiler presented here is really
just a translater from Python Bytecode to Web-Assembly.
Of course there are also big differences between Python Bytecode and
Web-Assembly.  The biggest one being that Python Bytecode is executed on the
Python virtual machine, which keeps a stack of Python objects, whereas
Web-Assembly is translated to native machine code and the stack is limited
to 32 and 64-bit integers and floating point numbers.  Nevertheless, if we
restrict our Python code to one of these types, we have very similar
systems.

The module `trans.py` contains an implementation of this "opcode transpiler".
At its core is a sequence of `if`..`elif` statements, which translate each
Python opcode into the equivalent Web-Assembly opcode.  The input to this
transpiler is syntactically Python but restricted to (64-bit) integer variables,
and only a few opcodes are implemented.  Nevertheless, we can generate
Web-Assembly for vary simple functions, and compare its execution speed to
Python and C.

Was an example for a speed comparison test, we have chosen the following
simple function (see `demo.py`, with the parameter `n` one billion):

    def foo(n):
        res = 0
        while n:
            res += n // 7
            n -= 1
        return res

The program `main.py` calls our transpiler, imports the WASM extension and
measures the execution time.  `demo.c` contains the C implementation of out
test function.  Here are our test speed results:

| Execution  | Time in seconds   | Remarks               |
| ---------- | ----------------- | --------------------- |
| Python     | 89.35             | Python 3.9            |
| WASM       |  0.96             | wasmtime 0.28.0       |
| C          |  3.21             | clang 11.0 with `-O0` |
| C          |  0.79             | clang 11.0 with `-O3` |

Interestingly, the WASM execution is faster than the C execution without
optimization, and only slightly slower than the optimized C code.
While we are able to achieve C speeds, we have to remember that this
transpiler is extremely simple, and only handles one integer type.
Extending the transpiler beyond that is a much harder task.
Another approach would be to compile Python to LLVM-IR using numba, and
then compile the intermediate representation to WASM.  Although this
involves additional steps, it might be an easier approach as one could
rely on existing libraries and code.
