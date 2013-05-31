PROBLEM = generate-prime-list
CONVERTER = primeList2txt

CFLAGS          = -std=c++11 -Wall -pedantic
DEBUGFLAGS      = -O0 -D _DEBUG -g
RELEASEFLAGS    = -O3 -D NDEBUG

make:
	g++ $(CFLAGS) $(RELEASEFLAGS) $(PROBLEM).cpp -o $(PROBLEM).out
	g++ $(CFLAGS) $(RELEASEFLAGS) $(CONVERTER).cpp -o $(CONVERTER).out
	
debug:
	g++ $(CFLAGS) $(DEBUGFLAGS) $(PROBLEM).cpp -o $(PROBLEM).out

clean:
	rm -rf  $(TARGET) *.class *.html *.log *.aux *.out *.bin
