# https://github.com/CVxTz/Recommender_keras
import numpy as np
from sklearn.metrics import mean_absolute_error
from utils import get_array, get_data, get_model_3

train, test, max_user, max_work, mapping_work = get_data('ml-20m/ratings.csv', nrows=100000)


# Train data analysis
# print(train.groupby('userId').aggregate({'movieId': 'count', 'rating': 'median', 'timestamp': ['min', 'max']}))
print(train.describe())
print((max_work, max_user))

np.random.seed(1)
model = get_model_3(max_work=max_work, max_user=max_user, latent_factors=50)
print(model.summary())

print(max(get_array(train["userId"])))

history = model.fit([get_array(train["movieId"]),
                     get_array(train["userId"])],
                     get_array(train["rating"]),
                    epochs=10,
                    # batch_size=13,
                    validation_split=0.2,
                    verbose=1)
model.save('model.h5')
predictions = model.predict([get_array(test["movieId"]), get_array(test["userId"])])

test_performance = mean_absolute_error(test["rating"], predictions)

print(" Test Mae model 3 : %s " % test_performance)
