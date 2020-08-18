#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <climits> // get maximum value of unsigned long long
#include <cstdlib> // exit
#include <algorithm> // std::max

#define SURPRESS_OUTPUT true
#define SHOW_DICT_CREATION false

using namespace std;

struct element {
    /** What is the next collatz number? */
    unsigned long long next;

    /** How many steps does it take until you reach 1? */
    unsigned long long steps;

    /** When you follow the collatz sequence of this number,
        what is the maximum you will get? */
    unsigned long long maxNumberInSequence;
};

map<unsigned long long, struct element> collatz;

unsigned long long CRITICAL_VALUE = (ULLONG_MAX-1) / 3;

unsigned long long maxAddFromOneEntry = 0;
unsigned long long maxEntry = 0;
unsigned long long maxStepsToOne = 0;
unsigned long long producesMaxStepsToOne = 1;
unsigned long long saveULong = 0;

/** n >= 1 */
unsigned long long nextCollatz(unsigned long long n) {
    if (n%2 == 0) {
        return n/2;
    } else {
        if (n >= CRITICAL_VALUE) {
            cerr << "Critical value is: " << CRITICAL_VALUE << endl;
            cerr << "n is: " << n << endl;
            cerr << "saveULong is: " << saveULong << endl;
            exit(1);
        }
        return 3*n+1;
    }
}

void insertCollatz(unsigned long long i){
    if (collatz.find(i) == collatz.end()) {
        if (SHOW_DICT_CREATION && !SURPRESS_OUTPUT) {
            cout << i << " is not in collatz:" << endl;
        }

        // i is not in collatz
        vector<unsigned long long> steps;
        unsigned long long current = i;
        unsigned long long next = nextCollatz(current);
        while(collatz.find(current) == collatz.end()) {
            steps.push_back(current);
            current = next;
            next = nextCollatz(current);
        }

        if (steps.size() > maxAddFromOneEntry) {
            maxAddFromOneEntry = steps.size();
        }

        vector<unsigned long long>::reverse_iterator it;
        for(it=steps.rbegin(); it != steps.rend(); it++){
            struct element el;
            el.next = current;
            el.steps = collatz[current].steps + 1;
            el.maxNumberInSequence = max(collatz[el.next].maxNumberInSequence, *it);
            collatz[*it] = el;

            if (el.steps > maxStepsToOne) {
                maxStepsToOne = el.steps;
                producesMaxStepsToOne = i;
            }

            if (*it > maxEntry) {
                maxEntry = *it;
            }

            current = *it;

            if (SHOW_DICT_CREATION && !SURPRESS_OUTPUT) {
                cout << "\tinserted " << *it << "->" << el.next << endl;
            }
        }

        return;
    } else if (SHOW_DICT_CREATION && !SURPRESS_OUTPUT) {
        cout << i << " was already in collatz." << endl;
    }
}

void printCollatz() {
    for(map<unsigned long long, struct element>::iterator it=collatz.begin();
        it!=collatz.end(); ++it) {
        unsigned long long next = (*it).first;
        while(next != 1) {
            cout << next << "->";
            next = collatz[next].next;
        }
        cout << 1 << endl;
    }
}

void print(unsigned long long max) {
    cout << "n,maximum,steps" << endl;
    for(unsigned long long i=1;i<=max;i++) {
        cout << i << ","
             << collatz[i].maxNumberInSequence << ","
             << collatz[i].steps << endl;
    }
}

int main(int argc, char* argv[]) {
    struct element e;
    e.next = 4;
    e.steps = 0;
    e.maxNumberInSequence = 4;
    collatz[1] = e;

    unsigned long long maxCollatz = (unsigned long long) atoi(argv[1]);

    for (unsigned long long i = 2; i <= maxCollatz; i++) {
        insertCollatz(i);
        saveULong = i;
        if (i % 1000000 == 0) {
            cerr << i << endl;
        }
    }

    cerr << "maxAddFromOneEntry: " << maxAddFromOneEntry << endl;
    cerr << "maxStepsToOne: " << maxStepsToOne
         << " (" << producesMaxStepsToOne << ")"<< endl;
    cerr << "maxEntry: " << maxEntry << endl;
    cerr << "entries: " << collatz.size() << endl;

    print(maxCollatz);

    return 0;
}
