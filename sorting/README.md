## Generate Data

This takes 30 minutes on my machine!

```bash
python generate_numbers.py -n 550_000_000
```

## Sort

```
$ time python radixsort-multi-thread.py

2020-05-29 07:44:57,389 INFO Generated files
2020-05-29 07:44:57,389 INFO Start splitting...
2020-05-29 07:49:49,945 INFO Done splitting...
Time for Chunking: 292.6s
Sort chunks: 252.0s
Written /home/moose/GitHub/MartinThoma/algorithms/sorting/radixsort_tmp/99.txt: 194.4
Merged chunks: 195.5s
Done!

real    740,22s
user    1894,14s
sys    192,17s
```
