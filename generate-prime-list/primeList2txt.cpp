#include <iostream>
#include <fstream>

using namespace std;

int main(int argc, char* argv[]) {
    FILE* pFile;
    pFile = fopen(argv[1], "rb");

    long long x;
    size_t read;
    while (!feof(pFile)) {
        read = fread(&x, sizeof(long long), 1, pFile);
        (void) read;
        cout << x << endl;
    }
    fclose(pFile);
}
