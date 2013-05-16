set terminal latex
set output "plot-tmp.tex"
set datafile separator "," 
set title "Collatz Number of steps"
plot '../steps.csv' every::1 
