PROBLEM = fractions-in-cpp

CFLAGS          = -std=c++11 -Wall -pedantic
DEBUGFLAGS      = -O0 -D _DEBUG -g
RELEASEFLAGS    = -O3 -D NDEBUG

make:
	g++ $(CFLAGS) $(RELEASEFLAGS) $(PROBLEM).cpp -o $(PROBLEM).out

debug:
	g++ $(CFLAGS) $(DEBUGFLAGS) $(PROBLEM).cpp -o $(PROBLEM).out

clean:
	rm -rf  $(TARGET) *.class *.html *.log *.aux *.out *.bin
