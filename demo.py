def foo(n):
    res = 0
    while n:
        res += n // 7
        n -= 1
    return res

if __name__ == '__main__':
    print(foo(1000_000_000))
