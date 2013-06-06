#include <iostream>
#include <string>
#include <gmpxx.h>

using namespace std;

mpz_class newton(int a, int n) {
    mpf_set_default_prec(1000000); // Increase this number.
    mpz_class x, aMPZ;
    aMPZ = a;
    x = a;
    for (int i=0; i<n; i++) {
        x = x - (x*x - aMPZ)/(2.0*x);
    }
    gmp_printf("%.10Ff\n", x.get_mpz_t()); // increase this number.
    return x;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        cout << "Please enter exactly two arguments." << endl;
        return 1;
    }
    int a = stoi(argv[1]);
    int n = stoi(argv[2]);

    newton(a, n);
    return 0;
}
