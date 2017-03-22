* `confusion-matrix.json`: The cell (line i, column j) represents how often
  members of class i were labeled with class j.
* `symbols.csv`: Line i contains the label for the symbol class i.


Run as

```
python visualize.py --cm confusion-matrices/cm-hasy-train-seq.json --labels labels/hasy.json --perm permutations/hasy-seq-test.json -n 100000
```