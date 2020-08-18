from collections import Counter
from itertools import combinations

import clana.io
import clana.visualize_cm
import networkx as nx
import numpy as np
import pandas as pd
import progressbar

# Load the data
df = pd.read_csv("movies.csv")
df["genres"] = df["genres"].str.split("|")

# Analyze the data
list_values = [value for valueset in df["genres"].tolist() for value in valueset]
value_count = Counter(list_values)

print("* Movies: {}".format(len(df)))
print("* Unique genres: {}".format(len(value_count)))
print("* Most common:")
most_common = sorted(value_count.items(), key=lambda n: n[1], reverse=True)
for name, count in most_common[:10]:
    print(f"    {count:>4}x {name}")

unique_genres = sorted(list(value_count.keys()))


def get_biggest_clusters(edges, n=10):
    G = nx.Graph()
    for authorset in edges.tolist():
        for author in authorset:
            G.add_node(author)

    for authorset in progressbar.progressbar(df["genres"].tolist()[:10_000]):
        for author1, author2 in combinations(authorset, 2):
            G.add_edge(author1, author2)

    print("Edges were added")

    components = [c for c in sorted(nx.connected_components(G), key=len, reverse=True)]
    return components[:n]


def create_matrix(nodes, edges):
    n2i = {node: i for i, node in enumerate(sorted(nodes))}
    # node to index
    mat = np.zeros((len(nodes), len(nodes)), dtype=np.int32)
    for edge in edges:
        for a, b in combinations(edge, 2):
            if a not in n2i or b not in n2i:
                continue
            mat[n2i[a]][n2i[b]] += 1
            if a != b:
                mat[n2i[b]][n2i[a]] += 1
    return mat, sorted(nodes)


components = get_biggest_clusters(df["genres"])
print("* Biggest clusters: {}".format([len(el) for el in components]))

component_w_publications = [(author, value_count[author]) for author in components[0]]
component_w_publications = sorted(
    component_w_publications, key=lambda n: n[1], reverse=True
)
authors = [author for author, count in component_w_publications[:1_00]]
mat, labels = create_matrix(authors, df["genres"].tolist())

clana.io.write_cm("genre-combinations.json", mat)
clana.io.write_labels("labels.json", labels)
clana.visualize_cm.main(
    "genre-combinations.json",
    perm_file="",
    steps=1_000_000,
    labels_file="labels.json",
    zero_diagonal=False,
    output="cm-genre-combinations.pdf",
)
