PROBLEM = sqrt-newton

CFLAGS          = -std=c++0x -Wall -pedantic
DEBUGFLAGS      = -O0 -D _DEBUG -g
RELEASEFLAGS    = -O3 -D NDEBUG

make:
	gcc sqrt-reference.c  -lgmp -lm -O0 -g3 -o reference.out
	g++ $(CFLAGS) $(RELEASEFLAGS) $(PROBLEM).cpp -o $(PROBLEM).out
	
debug:
	g++ $(CFLAGS) $(DEBUGFLAGS) $(PROBLEM).cpp -o $(PROBLEM).out

test:
	wc -l numbers.txt

clean:
	rm -rf  $(TARGET) *.class *.html *.log *.aux *.out *.txt
