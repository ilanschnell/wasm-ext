def foo():
    a = 42
    b = 7
    return a + b

def bar(n):
    return (1 + n) * n

def add(a, b):
    return a + b

def max(a, b):
    if a > b:
        c = a
    else:
        c = b
    return c


print(foo())
print(bar(5))
print(add(3, 4))
print(max(2, 9))
