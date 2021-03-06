def foo():
    a = 42
    b = 7
    return a + b

def bar(n):
    return (1 + n) * n

def add(a, b):
    return a + b

#def max(a, b):
#    if a > b:
#        c = a
#    else:
#        c = b
#    return c

def sum7(n):
    res = add(foo(), bar(3))
    while n:
        res += n // 7
        n -= 1
    return res


if __name__ == '__main__':
    print(foo())
    print(bar(5))
    print(add(3, 4))
    print(sum7(1000))

    import dis
    print(dis.show_code(sum7))
    print(dis.dis(sum7))
