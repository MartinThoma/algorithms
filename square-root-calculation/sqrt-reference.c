// Thanks to http://stackoverflow.com/a/15363123/562769
#include <stdio.h>
#include <gmp.h>

int main(int argc, char *argv[]) {
    if(argc<=1) {
        printf("Reference: Add one argument for a.\n");
        return 1;
    }
    mpf_t res, a;
    mpf_set_default_prec(1000000); // Increase this number.
    mpf_init(res);
    mpf_init(a);
    mpf_set_str(a, argv[1], 10);
    mpf_sqrt (res, a);
    gmp_printf("%.1000Ff\n", res); // increase this number.
    return 0;
}
