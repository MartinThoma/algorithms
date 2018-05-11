#!/usr/bin/python
# -*- coding: utf-8 -*-

r"""
Download Tweets. Similar to the one from Inaki San Vicente, but working.

The input file has to contain the tweet ids of the tweets to download in the
TREC microblog task format:

    tweetid<tab>userid<tab>language

The output is CSV:

           "statusId \t userId \t lang \t tweet_text\n"
           "statusId \t userId \t lang \t 'Not Available'\n"
           ...
"""

from bs4 import BeautifulSoup
import codecs
import re
import urllib

__version__ = '0.1'


def main(in_file, out_file):
    """Main file to parse the input, get tweets and return an output."""
    cache = {}

    for line in open(in_file):
        fields = unicode(line).rstrip(u'\n').split(u'\t')

        sid = fields[0]
        uid = fields[1]

        # url = 'http://twitter.com/%s/status/%s' % (uid, sid)
        # print "debug: "+uid+"  "+sid+"\n"

        text = u"Not Available"
        if sid in cache:
            text = cache[sid]
        else:
            try:
                # get status page
                f = urllib.urlopen("http://twitter.com/%s/status/%s" %
                                   (uid, sid))
                encoding = f.headers['content-type'].split('charset=')[-1]
                ucontent = unicode(f.read(), encoding)

                # parse with Beautiful soup
                html = ucontent.replace("</html>", "") + "</html>"
                soup = BeautifulSoup(html)
                # small elements contain the status ids
                small = soup.select("small > a")
                # p elements next to small elements have the tweet content
                p = soup.find_all("p", attrs={'class': "js-tweet-text"})
                # search for the tweet with the correct status id.
                for i in range(len(small)):
                    regex = re.escape(sid)
                    if re.search(regex, str(small[i])):
                        text = p[i].get_text()
                        cache[sid] = text
                        break

            except Exception:
                continue

        text = text.replace('\n', ' ')
        text = re.sub(r'\s+', ' ', text)

        with codecs.open(out_file, 'a+', encoding='utf-8') as file:
            file.write(u"\t".join(fields + [text]) + u"\n")


def get_parser():
    """Get parser object for script xy.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input",
                        dest="in_file",
                        help="File with Twitter IDs",
                        metavar="FILE",
                        required=True)
    parser.add_argument("-o", "--output",
                        dest="out_file",
                        help="Fetched data",
                        metavar="FILE",
                        required=True)
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.in_file, args.out_file)
