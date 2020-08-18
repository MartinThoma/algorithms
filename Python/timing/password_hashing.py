#!/usr/bin/env python

import random
import timeit

import numpy as np
from werkzeug.security import check_password_hash, generate_password_hash

random.seed(0)


def main():
    str_gen = "import random;random.seed(0);string=''.join(random.choices('ABCDEFGHIJKLM', k=20));"
    pw_gen = (
        "from werkzeug.security import generate_password_hash, check_password_hash;"
    )
    string_20 = "".join(random.choices("ABCDEFGHIJKLM", k=20))
    # string_2000 = ''.join(random.choices("ABCDEFGHIJKLM", k=2000))
    # string_200000 = ''.join(random.choices("ABCDEFGHIJKLM", k=200000))
    # string_200000000 = ''.join(random.choices("ABCDEFGHIJKLM", k=200000000))
    functions = [
        (
            "generate_password_hash(string, method='pbkdf2:sha512:1',salt_length=8)",
            "sha512, 1 iteration",
            str_gen + pw_gen,
        ),
        (
            "generate_password_hash(string, method='pbkdf2:sha512:15000',salt_length=8)",
            "sha512, 15000 iteration",
            str_gen + pw_gen,
        ),
        (
            "generate_password_hash(string, method='pbkdf2:sha256:15000',salt_length=8)",
            "sha256, 15000 iteration",
            str_gen + pw_gen,
        ),
        (
            "generate_password_hash(string, method='pbkdf2:sha512:1000',salt_length=8)",
            "sha512, 1000 iteration",
            str_gen + pw_gen,
        ),
        (
            "generate_password_hash(string, method='pbkdf2:sha256:1000',salt_length=8)",
            "sha256, 1000 iteration",
            str_gen + pw_gen,
        ),
        (
            "generate_password_hash(string, method='pbkdf2:md5:15000',salt_length=8)",
            "md5, 15000 iteration",
            str_gen + pw_gen,
        ),
    ]
    iter_list(
        functions,
        title="Password generation time",
        outfile="password-generation-time.png",
    )
    functions = [
        (
            "check_password_hash(pwhash=hash, password=string)",
            "sha512, 1 iteration",
            str_gen
            + pw_gen
            + "hash=generate_password_hash(\"{}\", method='pbkdf2:sha512:1', salt_length=8)",
        ),
        (
            "check_password_hash(pwhash=hash, password=string)",
            "sha512, 1000 iteration",
            str_gen
            + pw_gen
            + "hash=generate_password_hash(\"{}\", method='pbkdf2:sha512:1000', salt_length=8)",
        ),
        (
            "check_password_hash(pwhash=hash, password=string)",
            "sha256, 1000 iteration",
            str_gen
            + pw_gen
            + "hash=generate_password_hash(\"{}\", method='pbkdf2:sha256:1000', salt_length=8)",
        ),
        (
            "check_password_hash(pwhash=hash, password=string)",
            "sha512, 15000 iteration",
            str_gen
            + pw_gen
            + "hash=generate_password_hash(\"{}\", method='pbkdf2:sha512:15000', salt_length=8)",
        ),
        (
            "check_password_hash(pwhash=hash, password=string)",
            "sha256, 15000 iteration",
            str_gen
            + pw_gen
            + "hash=generate_password_hash(\"{}\", method='pbkdf2:sha256:15000', salt_length=8)",
        ),
        (
            "check_password_hash(pwhash=hash, password=string)",
            "md5, 15000 iteration",
            str_gen
            + pw_gen
            + "hash=generate_password_hash(\"{}\", method='pbkdf2:md5:15000', salt_length=8)",
        ),
    ]
    iter_list(
        functions,
        title="Password verification time",
        outfile="password-verification-time.png",
    )


def iter_list(functions, title, outfile):
    duration_list = {}
    for func, name, setup in functions:
        durations = timeit.repeat(func, repeat=100, number=3, setup=setup)
        duration_list[name] = list(np.array(durations) * 1000)
        print(
            "{func:<20}: "
            "min: {min:5.1f}μs, mean: {mean:5.1f}μs, max: {max:6.1f}μs".format(
                func=name,
                min=min(durations) * 10 ** 6,
                mean=np.mean(durations) * 10 ** 6,
                max=max(durations) * 10 ** 6,
            )
        )
        create_boxplot(title, duration_list, outfile=outfile)


def create_boxplot(title, duration_list, showfliers=False, outfile="out.png"):
    import operator

    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.figure(num=None, figsize=(8, 4), dpi=300, facecolor="w", edgecolor="k")
    sns.set(style="whitegrid")
    sorted_keys, sorted_vals = zip(
        *sorted(duration_list.items(), key=operator.itemgetter(0))
    )
    flierprops = dict(markerfacecolor="0.75", markersize=1, linestyle="none")
    ax = sns.boxplot(
        data=sorted_vals,
        width=0.3,
        orient="h",
        flierprops=flierprops,
        showfliers=showfliers,
    )
    ax.set(xlabel="Time in ms", ylabel="")
    plt.yticks(plt.yticks()[0], sorted_keys)
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(outfile)


if __name__ == "__main__":
    main()
