#include <iostream>
#include <fstream>

using namespace std;

int main(int argc, char* argv[]) {
    ifstream myFile (argv[1], ios::in | ios::binary);

    unsigned int x;
    while (!myFile.eof()) {
        myFile.read((char*)&x, sizeof(int));
        cout << x << endl;
    }
    myFile.close();
}
