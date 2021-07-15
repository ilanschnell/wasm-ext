#include <stdlib.h>  /* for int64_t */
#include <stdio.h>


int64_t foo(int64_t n)
{
    int64_t res = 0;

    while (n) {
        res += n / 7;
        n--;
    }
    return res;
}

int main()
{
    int64_t i = 1000 * 1000 * 1000;

    printf("%lld\n", foo(i));

    return 0;
}
