PROBLEM = invert-matrix

CFLAGS          = -std=c++0x -Wall -pedantic
DEBUGFLAGS      = -O0 -D _DEBUG -g
RELEASEFLAGS    = -O3 -D NDEBUG

make:
	g++ $(CFLAGS) $(RELEASEFLAGS) $(PROBLEM).cpp -o $(PROBLEM).out

debug:
	g++ $(CFLAGS) $(DEBUGFLAGS) $(PROBLEM).cpp -o $(PROBLEM).out

test:
	wc -l numbers.txt

clean:
	rm -rf  $(TARGET) *.class *.html *.log *.aux *.out
