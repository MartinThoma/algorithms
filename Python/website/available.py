import progressbar
import pythonwhois


def is_registered(site):
    """Check if a domain has an WHOIS record."""
    try:
        details = pythonwhois.get_whois(site)
    except pythonwhois.shared.WhoisException as e:
        print(f"Exception for {site}")
        print(e)
        return False
    return not details["raw"][0].startswith("No match for")


def read_from_file(path):
    with open(path) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def generate_by_pattern(pattern, prefixes=None):
    if prefixes is None:
        prefixes = [""]
    consonants = [
        "b",
        "c",
        "d",
        "f",
        "g",
        "h",
        "j",
        "k",
        "l",
        "m",
        "n",
        "p",
        "q",
        "r",
        "s",
        "t",
        "v",
        "w",
        "x",
        "z",
    ]
    vowels = ["a", "e", "i", "y", "o", "u"]
    part, rest = pattern[0], pattern[1:]
    data = []
    for prefix in prefixes:
        if part == "V":
            for el in vowels:
                part = prefix + el
                if len(rest) > 0:
                    data += generate_by_pattern(rest, part)
                else:
                    data.append(part)
        else:
            for el in consonants:
                part = prefix + el
                if len(rest) > 0:
                    data += generate_by_pattern(rest, part)
                else:
                    data.append(part)
    return data


# https://raw.githubusercontent.com/dominictarr/random-name/master/first-names.txt
names = read_from_file("english-adjectives.txt")
sites = [f"{name}.me" for name in names]
# https://raw.githubusercontent.com/datmt/English-Verbs/master/verbsList
# names = read_from_file('verbs.txt')
# sites = ['{}.it'.format(name) for name in names]
sites = [f"{name}.com" for name in generate_by_pattern("CVCV")]
print(len(sites))

i = 0
ava_sites = []
for site in progressbar.progressbar(sites):
    if " " in site:
        i += 1
        continue
    if not is_registered(site):
        print(site)
        ava_sites.append(site)
print(ava_sites)


# from joblib import Parallel, delayed
# import multiprocessing

# # what are your inputs, and what operation do you want to
# # perform on each input. For example...
# names = read_from_file('first-names.txt')
# def is_registered(site):
#     """Check if a domain has an WHOIS record."""
#     details = pythonwhois.get_whois(site)
#     return not details['raw'][0].startswith('No match for')

# num_cores = multiprocessing.cpu_count()

# results = Parallel(n_jobs=num_cores)(delayed(is_registered)(i) for i in sites)
# print(results)
