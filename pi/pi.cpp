#include <stdio.h>

using namespace std;

int main(int argc, char* argv[]) {
    double pi = 0;
    int sign = 1.0;
    for(int i=1;i<1000000000;i+=2){
        pi = pi + sign*4.0/i;
        sign *= -1;
    }

    printf("%.60f\n", pi);
    return 0;
}
