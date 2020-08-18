import random

import implicit
from scipy.sparse import csr_matrix

nb_movies = 50_000
nb_users = 10_000_000
nb_ratings = nb_users * 50
factors = 64

model = implicit.als.AlternatingLeastSquares(factors=factors)

print("Create movies which are rated...")
row = [random.randint(0, nb_movies) for i in range(nb_ratings)]

print("Create users which did rate...")
col = [random.randint(0, nb_users) for i in range(nb_ratings)]

print("Create ratings...")
data = [random.randint(0, 5) for i in range(nb_ratings)]


item_user_data = csr_matrix((data, (row, col)), shape=(max(row) + 1, max(col) + 1))
model.fit(item_user_data)
