#include <iostream>
#include <fstream>
#include <cstdlib>

using namespace std;

int randint(int min, int max) {
    return min + (rand() % (int)(max - min + 1));
}

int main (int argc, char* argv[]) {
    ofstream myfile;
    myfile.open ("numbers.txt");
    for (int i =0; i<1000000000; i++) {
        myfile << randint(-1000,1000) << "\n";
    }
    myfile.close();
    return 0;
}
