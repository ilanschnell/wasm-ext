#include <stdio.h>
#include <stdlib.h>             /* for int64_t */


int64_t collatz(int64_t n)
{
    int64_t j = 0;              /* result */

    while (n != 1) {
        n = n % 2 ? 3 * n + 1 : n / 2;
        j++;
    }
    return j;
}

int main(void)
{
    int64_t N = 100 * 1000 * 1000;
    int64_t i, j, m = 0;

    for (i = 1; i < N; i++) {
        if ((j = collatz(i)) > m) {
            m = j;
            printf("%3lld: %9lld\n", m, i);
        }
    }
    return 0;
}
