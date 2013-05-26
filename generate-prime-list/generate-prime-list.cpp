#include <stdio.h> // fopen
#include <iostream> // atoi
#include <vector>

using namespace std;

void sieveOfEratosthenes(unsigned int n) {
    FILE* pFile;
    pFile = fopen("huge-prime-list.bin", "wb");
    vector<bool> primesEratosthenes (n+1, true);

    for (unsigned int i=3; i<n; i+=2) {
        if (primesEratosthenes[i]) {
            fwrite(&i, sizeof(unsigned int), 1, pFile);
     
            for (unsigned int j=i*i; j<=n; j+=i) {
                primesEratosthenes[j] = false;
            }
        }
    }

    fclose(pFile);
}

int main(int argc, char* argv[]) {
    unsigned int n = (unsigned int) atoi(argv[1]);
    sieveOfEratosthenes(n);
    return 0;
}
