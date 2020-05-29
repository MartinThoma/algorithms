#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <map>
#include <vector>
#include <omp.h>

using namespace std;

vector<string> chunk_data(string big_filepath)
{
    vector<string> chunks_to_sort;
    map<string, ofstream* > prefix2file;
    system("mkdir cpp-radix");
    for (int i = 10; i < 100; ++i) {
        string prefix = to_string(i);
        prefix2file[prefix] = new ofstream("cpp-radix/" + prefix + ".txt");
        chunks_to_sort.push_back("cpp-radix/" + prefix + ".txt");
    }

    // Read and split the file
    ifstream infile(big_filepath);
    string line;
    cout << "start chunking" << endl;
    while (infile >> line) {
        *prefix2file[line.substr(0,2)] << line << '\n';
    }
    cout << "chunking done" << endl;

    // Close files
    for(map<string,ofstream*>::iterator it=prefix2file.begin();
        it!=prefix2file.end(); ++it) {
        (*it).second->close();
    }

    return chunks_to_sort;
}


void sort_chunk(string filepath)
{
    // Read
    vector<string> lines;
    ifstream infile(filepath);
    string line;
    while (infile >> line) {
        lines.push_back(line);
    }
    infile.close();

    // Sort
    sort(lines.begin(), lines.end());

    // write
    ofstream output_file(filepath);
    ostream_iterator<string> output_iterator(output_file, "\n");
    copy(lines.begin(), lines.end(), output_iterator);
    output_file.close();
}

void merge(vector<string> chunks)
{
    ofstream output_file("cpp-sorted.txt");
    ostream_iterator<string> output_iterator(output_file, "\n");

    // iterate over the vector
    vector<string>::iterator it_chunk;
    for(it_chunk=chunks.begin(); it_chunk != chunks.end(); it_chunk++) {
        cout << "Sort " << *it_chunk << endl;

        // Read file
        ifstream infile(*it_chunk);
        string line;
        while (infile >> line) {
            output_file << line << '\n';
        }
        infile.close();
    }

    output_file.close();
}


int main()
{
    vector<string> chunks_to_sort = chunk_data("numbers-large.txt");
    vector<string>::iterator it_chunk;

    #pragma omp parallel for
    for(it_chunk=chunks_to_sort.begin(); it_chunk != chunks_to_sort.end(); it_chunk++) {
        cout << "Sort " << *it_chunk << endl;
        sort_chunk(*it_chunk);
    }

    cout << "Merge" << endl;
    merge(chunks_to_sort);
    cout << "done" << endl;
    return 0;
}
