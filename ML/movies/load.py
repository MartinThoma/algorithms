import numpy as np
import pandas as pd
from scipy import spatial

df = pd.read_csv("imdb.csv", sep=",", error_bad_lines=False, escapechar="\\")
df = df.drop(columns=["fn", "tid", "wordsInTitle", "url"])

titles = df["title"].tolist()

similarities = np.zeros((len(titles), len(titles)))

df = df.replace(
    {"type": {"video.movie": 0, "video.episode": 1, "video.tv": 2, "game": 3}}
)
df = df.drop(columns=["title"])
features = np.zeros((len(titles), 39))
for i, el in enumerate(df.values):
    features[i] = el

for i in range(len(titles)):
    print(i)
    for j in range(len(titles)):
        if i == j:
            similarities[i][j] = 1
        elif j > i:
            similarities[i][j] = similarities[j][i]
        else:
            movie1 = features[i]
            movie2 = features[j]
            similarities[i][j] = 1 - spatial.distance.cosine(movie1, movie2)
