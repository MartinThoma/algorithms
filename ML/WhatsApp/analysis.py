#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Exploratory analysis of a whatsapp chat conversation."""

# core modules
from collections import Counter
import datetime
import os
import re

# 3rd party modules (you might have to install them via pip)
import pandas as pd
import matplotlib.pyplot as plt


def main(path):
    """Analyze a whatsapp chat file."""
    df = parse_file(path)
    df = augment_df(df)
    print_general_statistics(df)
    generate_visualizations(df)
    text_mining(df)
    return df


class Message(object):
    """A WhatsApp message object."""

    def __init__(self, line):
        self.line = line
        self.datetime = datetime.datetime.strptime(line[:17],
                                                   '%d/%m/%Y, %H:%M')
        if ':' not in line[20:]:
            self.sender = 'SYSTEM'
            self.text = line[20:]
        else:
            sender, text = line[20:].split(':', 1)
            text = text.strip()
            self.sender = sender
            self.text = text

    def __str__(self):
        return 'Message({:%y-%m-%d}, {})'.format(self.datetime, self.text[:30])

    __repr__ = __str__


def parse_file(path):
    """Parse a WhatsApp chat file into a dataframe."""
    with open(path) as f:
        data = f.read()
    messages = parse_into_messages(data)
    df = pd.DataFrame({'sender': [msg.sender for msg in messages],
                       'text': [msg.text for msg in messages],
                       'nb_words': [count_words(msg.text) for msg in messages],
                       'date': [msg.datetime for msg in messages]})
    return df


def augment_df(df):
    df['sender_before'] = df['sender'].shift(1)
    df['date_before'] = df['date'].shift(1)
    df['response_to'] = df['date_before']
    selector = df['sender_before'] == df['sender']
    df.loc[selector, 'response_to'] = None
    df['response_time'] = df['date'] - df['response_to']
    df['response_seconds'] = df['response_time'].dt.total_seconds()
    return df


def parse_into_messages(data):
    """
    Take on string which contains many messages and return list of message str.

    Parameters
    ----------
    data : str

    Returns
    -------
    messages : List[str]
    """
    tmp_msg = ''
    data = data.replace('<Media omitted>', 'MEDIA_OMITTED')
    lines = data.split('\n')
    messages = []
    whatsapp_date_pattern = re.compile(r'\d{2}/\d{2}/\d{4}, \d{2}:\d{2}')
    for line in lines:
        if whatsapp_date_pattern.match(line):
            if len(tmp_msg) > 17:
                messages.append(Message(tmp_msg))
            tmp_msg = line
        else:
            tmp_msg += '\n' + line
    return messages


def count_words(text):
    """Count the words in a text."""
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    return len(tokens)


def generate_visualizations(df):
    """Generate many visualizations for a whatsapp chat df."""
    visualize(df,
              grouping=(df['date'].dt.hour),
              column_name='date',
              title='Send+received messages by hour',
              xlabel='hour of the day (local time)',
              filename='messages_by_hour.png')

    # Weekend
    df_weekday = df[df['date'].dt.weekday.isin([0, 1, 2, 3, 4])]
    df_weekend = df[df['date'].dt.weekday.isin([5, 6])]
    text = ' '.join(df.text.tolist()).lower()
    create_wordcloud(text)
    visualize(df_weekday,
              grouping=(df_weekday['date'].dt.hour),
              column_name='date',
              title='Send+received messages by hour (weekday only)',
              xlabel='hour of the day (local time)',
              filename='messages_by_hour_weekday.png')
    visualize(df_weekend,
              grouping=(df_weekend['date'].dt.hour),
              column_name='date',
              title='Send+received messages by hour (weekend only)',
              xlabel='hour of the day (local time)',
              filename='messages_by_hour_weekend.png')

    visualize(df,
              grouping=(df['date'].dt.weekday),
              column_name='date',
              title='Send+received messages by weekday',
              xlabel='From Monday=0 to Sunday=6',
              filename='messages_by_weekday.png')
    df2 = df[df['date'] > df.date.max() - datetime.timedelta(days=365)]
    visualize(df2,
              grouping=(df2['date'].dt.month),
              column_name='date',
              title='Send+received messages by month',
              filename='messages_by_month.png')
    visualize(df,
              grouping=[df['date'].dt.year, df['date'].dt.week],
              column_name='date',
              title='Send+received messages over time',
              filename='messages_over_time.png')


def visualize(df,
              grouping,
              column_name='start_date',
              color='#494949',
              title='',
              xlabel='',
              filename='image.png'):
    """
    Visualize a dataframe with a date column.

    Parameters
    ----------
    df : Pandas dataframe
    column_name : str
        Column to visualize
    color : str
    title : str
    """
    plt.figure(figsize=(20, 10))

    ax = (df[column_name].groupby(by=grouping)
                         .count()).plot(kind="bar", color=color, stacked=True)  # .unstack()

    ax.set_facecolor('#eeeeee')
    ax.set_xlabel(xlabel)
    ax.set_ylabel("count")
    ax.set_title(title)
    plt.savefig(os.path.join('images', filename))


def print_general_statistics(df):
    print('{nb_messages} messages exchanged between {start_date} and '
          '{end_date} ({time})'
          .format(nb_messages=len(df),
                  start_date=df['date'].min(),
                  end_date=df['date'].max(),
                  time=df['date'].max() - df['date'].min()))
    print(df['sender'].value_counts())
    print(df.groupby('sender').aggregate({'nb_words': sum}))
    print('Message length distribution:')
    senders = [sender for sender in df.sender.unique() if sender != 'SYSTEM']
    for sender in senders:
        df_sender = df[df.sender == sender]
        print('## {}'.format(sender))
        print('\tmin-words: {}'.format(df_sender['nb_words'].min()))
        print('\tmean-words: {:0.0f}'.format(df_sender['nb_words'].mean()))
        print('\tmax-words: {}'.format(df_sender['nb_words'].max()))
        print('\t---')
        print('\tmin-chars: {}'.format(df_sender['text'].str.len().min()))
        print('\t.25-chars: {}'.format(df_sender['text'].str.len().quantile(0.25)))
        print('\tmean-chars: {:0.0f}'.format(df_sender['text'].str.len().mean()))
        print('\t.95-chars: {}'.format(df_sender['text'].str.len().quantile(0.95)))
        print('\tmax-chars: {}'.format(df_sender['text'].str.len().max()))

    print('## After how many seconds do people react?')
    df_humans = df[df.sender != 'SYSTEM']
    print(df_humans.groupby('sender')
                   .agg({'response_seconds': ['median', 'mean', 'max']}))


def text_mining(df):
    df_humans = df[df.sender != 'SYSTEM']

    corpus = ' '.join(df.text.tolist()).lower()
    overall_counter = Counter(corpus.split(' '))
    print('## Most common 30 words')
    print(overall_counter.most_common(30))

    senders = [sender for sender in df.sender.unique() if sender != 'SYSTEM']
    for sender in senders:
        print('## {}'.format(sender))
        df_sender = df[df.sender == sender]
        corpus = ' '.join(df_sender.text.tolist()).lower()
        print('### Most common 30 words')
        print(Counter(corpus.split(' ')).most_common(30))

    print('## Smiley Analysis')
    smiley_analysis(df_humans)


def smiley_analysis(df):
    smileys = find_common_smileys(df)
    senders = df.sender.unique()
    smiley_counts = {}
    for smiley in smileys:
        smiley_counts[smiley] = []
        for sender in senders:
            count = sum(df[df.sender == sender].text.str.count(smiley))
            smiley_counts[smiley].append(count)
    df2 = pd.DataFrame(smiley_counts, index=senders)
    df2 = df2.T
    print(df2)


def find_common_smileys(df, most_common=20):
    text = ' '.join(df.text.tolist())
    text = [el for el in text if ord(el) > 1000]
    special_chars = Counter(text)
    special_chars = [char for char, count in special_chars.most_common(20)]
    return special_chars


def create_wordcloud(text, output='wordcloud.png'):
    # Start with loading all necessary libraries
    from wordcloud import WordCloud

    # Create and generate a word cloud image:
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    import random

    def love_color_func(word, font_size, position, orientation, random_state=None,
                        **kwargs):
        val = random.randint(0, 200)
        return (250, val, val)

    stop_words = set(stopwords.words('german')).union(set(['dass', 'media_omitted']))
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if w not in stop_words]
    text = ' '.join(filtered_sentence)

    wordcloud = WordCloud(width=800, height=1200,
                          # max_font_size=50,
                          # max_words=100,
                          background_color="white").generate(text)
    wordcloud.recolor(color_func=love_color_func, random_state=3)

    # Display the generated image:
    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(os.path.join('images', output), dpi=300, bbox_inches='tight')


def is_valid_file(parser, arg):
    """
    Check if arg is a valid file that already exists on the file system.

    Parameters
    ----------
    parser : argparse object
    arg : str

    Returns
    -------
    arg
    """
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def get_parser():
    """Get parser object for whatsapp analysis script."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file",
                        dest="filename",
                        type=lambda x: is_valid_file(parser, x),
                        required=True,
                        help="Whatsapp file to analyze",
                        metavar="FILE")
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args.filename)
