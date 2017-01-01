FLAGS += -std=c++0x
#FLAGS += -std=c++11

FLAGS += -Wall -Wextra -pedantic
FLAGS += -Ofast
#FLAGS += -D__OPENCV_OBJDETECT_HPP__
FLAGS +=  `pkg-config opencv --cflags --libs`
FLAGS +=  -lboost_system -lboost_program_options -lboost_serialization -lboost_filesystem

assignment3: *.cc
	$(CXX) -o $@ main.cc $(FLAGS)

.PHONY : clean

clean:
	rm -f assignment3 graph.txt ROC.png score.txt
