#include <iostream>
#include <fstream>

using namespace std;

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cout << "You have to specify a file name" << endl;
    } else {
        FILE* pFile;
        pFile = fopen(argv[1], "rb");

        long long x;
        size_t read;
        while (!feof(pFile)) {
            read = fread(&x, sizeof(long long), 1, pFile);
            (void) read;
            if (feof(pFile)){
                break; // otherwise it duplicates the last entry
            }
            cout << x << endl;
        }
        fclose(pFile);
    }
}
