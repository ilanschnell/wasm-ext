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
