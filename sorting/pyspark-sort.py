from pyspark import SparkContext

sc = SparkContext("local", "Max Temperature")

print("Read file")
text_file = sc.textFile("numbers-large.txt")  # hdfs://...

print("Sort file")
counts = text_file.sort()

print("Write file")
counts.saveAsTextFile("numbers-spark-sorted.txt")
