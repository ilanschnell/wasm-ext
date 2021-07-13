import ast
import dis
import inspect


t_op = {p + k: v for p in ('BINARY_', 'INPLACE_') for k, v in {
    'ADD': 'add',
    'SUBTRACT': 'sub',
    'MULTIPLY': 'mul',
    'FLOOR_DIVIDE': 'div_s',
    'TRUE_DIVIDE': 'div_s',
    'MODULO': 'rem_s',
    'AND': 'and',
    'OR': 'or',
    'XOR': 'xor',
    'LSHIFT': 'shl',
    'RSHIFT': 'shr_s'
}.items()}

t_cmp = {
    '<': 'lt_s',
    '<=': 'le_s',
    '==': 'eq',
    '!=': 'ne',
    '>': 'gt_s',
    '>=': 'ge_s',
}

header = [
    '(module',
    '(func $unary_negative', '(param i64)', '(result i64)',
    'i64.const 0',
    'local.get 0',
    'i64.sub', ')']

def disp_code(code):
    print('----- %s -----' % code.co_name)
    for name in dir(code):
        if name.startswith('co_'):
            print('%-20s  %s' % (name, code.__getattribute__(name)))

def disp_op(op):
    print('%s %3d %-25s  %s %s' % (
        '>>' if op.is_jump_target else '  ',
        op.offset, op.opname,
        '' if op.arg is None else '%4d' % op.arg,
        '' if op.argval is None else '(%s)' % op.argval))

def t_function(f, w_mod, f_names, debug=False):
    assert inspect.iscode(f)
    labels = dis.findlabels(f.co_code)
    if debug:
        disp_code(f)
        print('labels: %s' % labels)

    w_mod.append('(func $%s' % f.co_name)
    if f.co_argcount:
        w_mod.append('(param %s)' % ' '.join(f.co_argcount * ['i64']))

    w_mod.append('(result i64)')
    nlocals = f.co_nlocals - f.co_argcount
    assert nlocals >= 0
    if nlocals:
        w_mod.append('(local %s)' % ' '.join(nlocals * ['i64']))

    f_stack = []

    for op in dis.get_instructions(f):
        opname = op.opname
        if debug:
            disp_op(op)

        if op.is_jump_target:
            assert op.offset in labels
            if op.offset == labels[1]:
                w_mod.extend(['(block', '(loop'])
            if op.offset == labels[0]:
                w_mod.extend([')', ')'])

        if opname in t_op:
            w_mod.append('i64.%s' % t_op[opname])

        elif opname == 'UNARY_POSITIVE':
            pass

        elif opname == 'UNARY_NEGATIVE':
            w_mod.extend(['call $unary_negative'])

        elif opname == 'LOAD_CONST':
            w_mod.append('i64.const %d' % f.co_consts[op.arg])

        elif opname == 'LOAD_FAST':
            w_mod.append('local.get %d  ;; %s' %
                         (op.arg, f.co_varnames[op.arg]))

        elif opname == 'STORE_FAST':
            w_mod.append('local.set %d  ;; %s' %
                         (op.arg, f.co_varnames[op.arg]))

        elif opname == 'COMPARE_OP':
            cmp_op = dis.cmp_op[op.arg]
            w_mod.append('i64.' + t_cmp[cmp_op])

        elif opname == 'LOAD_GLOBAL':
            name = f.co_names[op.arg]
            if name in f_names:
                f_stack.append(name)
            else:
                raise NotImplementedError("%s (%s)" % (opname, name))

        elif opname == 'CALL_FUNCTION':
            w_mod.append('call $%s' % f_stack.pop())

        elif opname == 'POP_JUMP_IF_FALSE':
            w_mod.extend(['i64.eqz', 'br_if 1'])

        elif opname == 'JUMP_ABSOLUTE':
            w_mod.append('br 0')

        elif opname == 'RETURN_VALUE':
            w_mod.append('return')

        else:
            raise NotImplementedError(opname)

    w_mod.append(')  ;; func %s' % f.co_name)


def t_module(source_text, filename='<module>', debug=False):
    module_ast = ast.parse(source_text)
    #print(ast.dump(module_ast, indent=4, include_attributes=True))
    co = compile(module_ast, filename, 'exec')
    #dis.dis(co)

    functions = [c for c in co.co_consts if inspect.iscode(c)]

    w_mod = list(header)
    for f in functions:
        t_function(f, w_mod,
                   [g.co_name for g in functions],
                   debug=debug)
    for f in functions:
        w_mod.append('(export "%s" (func $%s))' % (f.co_name, f.co_name))
    w_mod.append(')')

    # indent output
    out = []
    indent = 0
    for x in w_mod:
        x = x.strip()
        out.append((indent - x.startswith(')')) * '    ' + x + '\n')
        indent += x.count('(')
        indent -= x.count(')')
    assert indent == 0
    return ''.join(out)


def t_file(py_file, wat_file, debug=False):
    with open(py_file) as fi:
        src = fi.read()

    dst = t_module(src, py_file, debug=debug)

    with open(wat_file, 'w') as fo:
        fo.write(dst)
