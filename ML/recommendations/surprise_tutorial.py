import zipfile

from surprise import SVD, Dataset, Reader, evaluate

# Unzip ml-100k.zip
zipfile = zipfile.ZipFile('ml-100k.zip', 'r')
zipfile.extractall()
zipfile.close()

# Read data into an array of strings
with open('./ml-100k/u.data') as f:
    all_lines = f.readlines()

# Prepare the data to be used in Surprise
reader = Reader(line_format='user item rating timestamp', sep='\t')
data = Dataset.load_from_file('./ml-100k/u.data', reader=reader)

# Split the dataset into 5 folds and choose the algorithm
data.split(n_folds=5)
algo = SVD()

# Train and test reporting the RMSE and MAE scores
evaluate(algo, data, measures=['RMSE', 'MAE'])

# Retrieve the trainset.
trainset = data.build_full_trainset()
algo.train(trainset)

# Predict a certain item
userid = str(196)
itemid = str(302)
actual_rating = 4
print(algo.predict(userid, itemid, actual_rating))
