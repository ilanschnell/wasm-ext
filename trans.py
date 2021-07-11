import dis
import inspect


t_op = {
    'BINARY_ADD': 'add',
    'BINARY_MULTIPLY': 'mul',
    'BINARY_FLOOR_DIVIDE': 'div_s',
    'INPLACE_ADD': 'add',
    'INPLACE_SUBTRACT': 'sub',
}

t_cmp = {
    '<': 'lt_s',
    '<=': 'le_s',
    '==': 'eq',
    '!=': 'ne',
    '>': 'gt_s',
    '>=': 'ge_s',
}

def t_function(f, w_mod, debug=False):
    assert inspect.iscode(f)

    labels = dis.findlabels(f.co_code)

    w_mod.append('(func $%s' % f.co_name)
    if f.co_argcount:
        w_mod.append('(param %s)' % ' '.join(f.co_argcount * ['i64']))

    w_mod.append('(result i64)')
    nlocals = f.co_nlocals - f.co_argcount
    assert nlocals >= 0
    if nlocals:
        w_mod.append('(local %s)' % ' '.join(nlocals * ['i64']))

    for op in dis.get_instructions(f):
        opname = op.opname

        if op.is_jump_target:
            assert op.offset in labels
            if op.offset == labels[1]:
                w_mod.append('(block (loop')
            if op.offset == labels[0]:
                w_mod.append('))')

        if opname in t_op:
            w_mod.append('i64.%s' % t_op[opname])

        elif opname == 'LOAD_CONST':
            w_mod.append('i64.const %d' % f.co_consts[op.arg])

        elif opname == 'LOAD_FAST':
            w_mod.append('local.get %d' % op.arg)

        elif opname == 'STORE_FAST':
            w_mod.append('local.set %d' % op.arg)

        elif opname == 'COMPARE_OP':
            cmp_op = dis.cmp_op[op.arg]
            w_mod.append('i64.' + t_cmp[cmp_op])

        elif opname == 'POP_JUMP_IF_FALSE':
            w_mod.append('i64.eqz  br_if 1')

        elif opname == 'JUMP_ABSOLUTE':
            w_mod.append('br 0')

        elif opname == 'RETURN_VALUE':
            pass

        else:
            raise ValueError("unknwon opcode: %s" % opname)

        if debug:
            print('%s %3d %-25s  %s %s' % (
                '>>' if op.is_jump_target else '  ',
                op.offset, opname,
                '' if op.arg is None else '%4d' % op.arg,
                '' if op.argval is None else '(%s)' % op.argval))

    w_mod.append(')')  # (func
