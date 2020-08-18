from collections import Counter
from itertools import combinations

import clana.io
import clana.visualize_cm
import networkx as nx
import numpy as np
import pandas as pd
import progressbar

# Load the data
df = pd.read_csv("articles.csv")
df["author"] = df["author"].str.split("::")

# Analyze the data
df = df[~df["author"].isna()]
authors = [author for authorset in df["author"].tolist() for author in authorset]
author_count = Counter(authors)

print("* Publications: {}".format(len(df)))
print("* Unique elements: {}".format(len(author_count)))
print("* Most common:")
most_common = sorted(author_count.items(), key=lambda n: n[1], reverse=True)
for name, count in most_common[:10]:
    print(f"    {count:>4}x {name}")

unique_authors = sorted(list(author_count.keys()))


def get_biggest_clusters(edges, n=10):
    G = nx.Graph()
    for authorset in edges.tolist():
        for author in authorset:
            G.add_node(author)

    for authorset in progressbar.progressbar(df["author"].tolist()[:10_000]):
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


components = get_biggest_clusters(df["author"])
print("* Biggest clusters: {}".format([len(el) for el in components]))

component_w_publications = [(author, author_count[author]) for author in components[0]]
component_w_publications = sorted(
    component_w_publications, key=lambda n: n[1], reverse=True
)
authors = [author for author, count in component_w_publications[:1_00]]
mat, labels = create_matrix(authors, df["author"].tolist())

clana.visualize_cm.main(
    "coauthors.json",
    perm_file="",
    steps=1_000_000,
    labels_file="labels.json",
    zero_diagonal=False,
    output="cm-ordered.pdf",
)
clana.io.write_cm("coauthors.json", mat)
clana.io.write_labels("labels.json", labels)
