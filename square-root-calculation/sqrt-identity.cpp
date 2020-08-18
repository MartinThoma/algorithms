#include <iostream>
#include <cmath>

using namespace std;

long double ln(int S, int n) {
    long double tmp = S - 1;
    long double result = tmp;
    long double sign = 1.0;
    for (int i=2; i<n/2; i++) {
        tmp *= (S-1);
        sign *= -1;
        result += sign*tmp/i;
    }
    return result;
}

long double e(long double x, int n) {
    long double numerator = 1;
    long double denominator = 1;
    long double result = 1;
    for (int i=1; i<n/2; i++) {
        numerator *= x;
        denominator *= i;
        result += numerator/denominator;
    }
    return result;
}

long double e2(long double x, int n) {
    long double numerator1 = x;
    long double numerator2 = x;
    long double denominator = 1;
    long double result = 1;
    for (int i=1; i<n/2; i++) {
        numerator2 += 2;
        denominator *= (2*i-1)*(2*i);
        result += (numerator1*numerator2)/denominator;
        numerator1 *= x*x;
    }
    return result;
}

long double sqrt(int a, int n) {
    return e2(ln(a, n)*0.5, n);
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        cout << "Please enter exactly two arguments." << endl;
        return 1;
    }
    int a = atoi(argv[1]);
    int n = atoi(argv[2]);
    printf("%.80Lf\n", sqrt(a, n));
    return 0;
}
