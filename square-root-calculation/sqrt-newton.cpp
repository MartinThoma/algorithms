#include <iostream>
#include <cmath>
 
using namespace std;
 
long double newton(int a, int n) {
    long double x = ((long double)a)/2;
    for (int i=0; i<n; i++) {
        x = x - (x*x - a)/(2*x);
    }
    return x;
}
 
int main(int argc, char *argv[]) {
    if (argc != 3) {
        cout << "Please enter exactly two arguments." << endl;
        return 1;
    }
    int a = atoi(argv[1]);
    int n = atoi(argv[2]);
    printf("%.80Lf\n", newton(a, n));
    return 0;
}
