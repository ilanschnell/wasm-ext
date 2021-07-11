#include <stdlib.h>             /* for int64_t */
#include <stdio.h>


int64_t sum(uint64_t n)
{
    int64_t res = 0;

    while (n > 0) {
        res += n;
        n--;
    }
    return res;
}

int main()
{
    int64_t i;

    for (i = 0; i < 5; i++)
        printf("%lld %lld\n", i, sum(i));

    i = 1000000000;
    printf("%lld\n", sum(i));

    return 0;
}
