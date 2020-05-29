import dask
import dask.dataframe as dd

input_file = "numbers-large.txt"
output_file = "numbers-large-sorted-dask.txt"
blocksize = 1_000_000

print("Create ddf")
ddf = dd.read_csv(input_file, header=None, blocksize=blocksize)

print("Sort")
ddf_sorted = ddf.set_index(0)

print("Write")
fut = ddf_sorted.to_csv(output_file, compute=False, single_file=True, header=None)
dask.compute(fut)
print("Stop")
