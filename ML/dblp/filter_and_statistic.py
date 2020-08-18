"""Filter and summarize dataset."""
import codecs
from collections import Counter, OrderedDict

import matplotlib.pyplot as plt
import numpy as np
import ujson
from nltk import word_tokenize
from tqdm import tqdm

# top 10 journals
journals = [
    "IEICE Transactions",
    "Applied Mathematics and Computation",
    "IEEE Trans. Information Theory",
    "Discrete Mathematics",
    "Sensors",
    "Theor. Comput. Sci.",
    "European Journal of Operational Research",
    "IEEE Trans. Signal Processing",
    "Neurocomputing",
    "IACR Cryptology ePrint Archive",
]

# 11~20
# , 'Commun. ACM',
#             'Bioinformatics', 'Expert Syst. Appl.', 'IEEE Trans. Communications', 'NeuroImage', 'Automatica',
#             'IEEE Trans. Industrial Electronics', 'Inf. Sci.', 'IEEE Trans. Computers',
#             'IEEE Trans. Geoscience and Remote Sensing'

def load_json(filename):
    with codecs.open(filename, mode="r", encoding="utf8", errors="ignore") as f:
        data = ujson.load(f)
        return data


def write_to_file(dataset, filename):
    with codecs.open(filename, mode="w", encoding="utf8") as f_out:
        for d in dataset.items():
            f_out.write("{}\t{}\n".format(d[0], d[1]))


def plot(features, save_name, title_name):
    x = list(features.keys())
    y = list(features.values())
    elem_size = len(features)
    color_map = plt.cm.get_cmap("RdYlBu_r")
    colors = [color_map(i / elem_size) for i in range(0, elem_size)]
    fig, ax = plt.subplots()
    fig.set_size_inches(16, 16)
    width = 0.75  # the width of the bars
    ind = np.arange(len(y))  # the x locations for the groups
    ax.barh(ind, y, width, color=colors)
    ax.set_yticks(ind)
    ax.set_yticklabels(x, minor=False)
    plt.title(title_name)
    for i, v in enumerate(y):
        ax.text(v, i, str(v), color="black", va="center")
    fig.savefig(save_name, dpi=100)
    plt.show()


def filter_records(dataset, save_path):
    results = []
    for record in tqdm(dataset, desc="Filter records"):
        title, author, year, journal, pages = (
            record["title"][0],
            record["author"],
            record["year"][0],
            record["journal"][0],
            record["pages"][0],
        )
        if journal == "IACR Cryptology ePrint Archive":
            print("\t".join([title, ", ".join(author), year, journal, pages]))
        # pre-defined method to filter records
        tokens = word_tokenize(title)
        if len(tokens) < 4 or len(tokens) > 20:
            continue
        if int(year) < 1980:
            continue
        if len(author) > 6:
            continue
        if journal not in journals:
            continue
        if int(pages) < 2 or int(pages) > 40:
            continue
        results.append(record)
    with codecs.open(save_path, mode="w", encoding="utf8") as f:
        ujson.dump(results, f)
    return results


def summarize(dataset):
    title_vocab, title_len, author_len, year_range, page_vocab, journal_vocab = (
        Counter(),
        Counter(),
        Counter(),
        Counter(),
        Counter(),
        Counter(),
    )
    author_vocab, year_vocab, all_vocab = Counter(), Counter(), Counter()  # char vocab
    for record in tqdm(dataset, desc="Summarize"):
        title, authors, year, journal, pages = (
            record["title"][0],
            record["author"],
            record["year"][0],
            record["journal"][0],
            record["pages"][0],
        )
        # process title
        tokens = word_tokenize(title)
        title_len[len(tokens)] += 1
        for token in tokens:
            title_vocab[token] += 1  # update title word vocab
            for char in token:
                all_vocab[char] += 1  # update all char vocab
        # process author (only char vocab)
        author_len[len(authors)] += 1
        for author in authors:
            for char in author:
                author_vocab[char] += 1  # update author char vocab
                all_vocab[char] += 1  # update all char vocab
        # process year (only char vocab)
        year_range[year] += 1
        for char in year:
            year_vocab[char] += 1  # update year char vocab
            all_vocab[char] += 1  # update all char vocab
        # process journal
        journal_vocab[journal] += 1  # update journal word vocab
        for char in journal:
            all_vocab[char] += 1  # update all char vocab
        # process pages
        page_vocab[pages] += 1  # update pages word vocab
        for char in pages:
            all_vocab[char] += 1  # update all char vocab
    # ordered
    title_vocab = OrderedDict(title_vocab.most_common())
    title_len = OrderedDict(sorted(title_len.items(), key=lambda t: int(t[0])))
    author_vocab = OrderedDict(author_vocab.most_common())
    author_len = OrderedDict(sorted(author_len.items(), key=lambda t: int(t[0])))
    year_vocab = OrderedDict(year_vocab.most_common())
    year_range = OrderedDict(sorted(year_range.items(), key=lambda t: int(t[0])))
    journal_vocab = OrderedDict(journal_vocab.most_common())
    page_vocab = OrderedDict(page_vocab.most_common())
    page_range = OrderedDict(sorted(page_vocab.items(), key=lambda t: int(t[0])))
    all_vocab = OrderedDict(all_vocab.most_common())
    # write to file
    save_path = "summary/{}.txt"
    write_to_file(title_vocab, save_path.format("title_vocab"))
    write_to_file(author_vocab, save_path.format("author_vocab"))
    write_to_file(year_vocab, save_path.format("year_vocab"))
    write_to_file(journal_vocab, save_path.format("journal_vocab"))
    write_to_file(page_vocab, save_path.format("page_vocab"))
    write_to_file(all_vocab, save_path.format("all_vocab"))
    # plot
    img_path = "summary/{}.png"
    plot(title_len, img_path.format("title_length"), "Distribution of Title's Length")
    plot(
        author_len, img_path.format("author_length"), "Distribution of Author's Length"
    )
    plot(year_range, img_path.format("year_range"), "Distribution of Year's Range")
    plot(journal_vocab, img_path.format("journal"), "Distribution of Journal")
    plot(page_range, img_path.format("page"), "Distribution of Page")
    # statistics
    aver_title_len = float(sum([int(x) * y for x, y in title_len.items()])) / sum(
        [x for x in title_len.values()]
    )
    aver_author_len = float(sum([int(x) * y for x, y in author_len.items()])) / sum(
        [x for x in author_len.values()]
    )
    print("Total number of records in dataset: {}".format(len(dataset)))
    print(
        "Average title length: {}, average author length: {}".format(
            aver_title_len, aver_author_len
        )
    )


def main():
    dataset = load_json("dataset/article.json")
    results = filter_records(dataset, "dataset/article_tiny.json")
    summarize(results)


if __name__ == "__main__":
    main()
