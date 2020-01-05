from collections import Counter
from itertools import combinations

import networkx as nx
import numpy as np
import pandas as pd
import progressbar

# Load the data
df = pd.read_csv("articles.csv")
df["author"] = df["author"].str.split("::")
print("len(df)={}".format(len(df)))
df = df[~df["author"].isna()]
print("len(df)={}".format(len(df)))
df = df[df["author"].apply(len) > 1]
print("len(df)={}".format(len(df)))
df = df.sort_values(by=["year", "journal"])
print(df)

print(df["author"].tolist()[:2])


def get_biggest_clusters(edges):
    G = nx.Graph()
    for authorset in edges.tolist():
        for author in authorset:
            G.add_node(author)

    for authorset in progressbar.progressbar(df["author"].tolist()[:100_000]):
        for author1, author2 in combinations(authorset, 2):
            G.add_edge(author1, author2)

    print("Edges were added")

    components = [
        len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)
    ]
    print(components[:10])


get_biggest_clusters(df["author"])
