import dis, inspect


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

    w_mod.append('(func $%s' % f.co_name)
    if f.co_argcount:
        w_mod.append('(param %s)' % ' '.join(f.co_argcount * ['i32']))

    w_mod.append('(result i32)')
    if f.co_nlocals:
        w_mod.append('(local %s)' % ' '.join(f.co_nlocals * ['i32']))

    for op in dis.get_instructions(f):
        opname = op.opname

        if op.is_jump_target:
            if op.offset == 4:
                w_mod.append('(block (loop')
            if op.offset == 30:
                w_mod.append('))')

        if opname in t_op:
            w_mod.append('i32.%s' % t_op[opname])

        elif opname == 'LOAD_CONST':
            w_mod.append('i32.const %d' % f.co_consts[op.arg])

        elif opname == 'LOAD_FAST':
            w_mod.append('local.get %d' % op.arg)

        elif opname == 'STORE_FAST':
            w_mod.append('local.set %d' % op.arg)

        elif opname == 'COMPARE_OP':
            cmp_op = dis.cmp_op[op.arg]
            w_mod.append('i32.' + t_cmp[cmp_op])

        elif opname == 'POP_JUMP_IF_FALSE':
            w_mod.append('i32.eqz  br_if 1')

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

    w_mod.append(')')
