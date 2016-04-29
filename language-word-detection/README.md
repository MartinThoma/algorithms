The question I want to tackle here is

> How to determine if character sequence is English word or not?

I got to it by [this SO question](http://datascience.stackexchange.com/q/11489/8820)
which is inspired by [a competition](https://github.com/hola/challenge_word_classifier).
The catch of it: The whole program (with data) has to be in a single file
which my not be larger than 64KiB.


## Exact solutions

Exact solutions are ones which are always completely right. 100% accuracy.

### Try 1: Word list

A list of words of the english language is [here](http://stackoverflow.com/q/2213607/562769).
I use [word2](https://github.com/dwyl/english-words).

The list has 235886 words and is 2.5 MB big. Even when compressed with 7z it
still has 637.2 KB.


### Try 2: Prefix tree

That didn't work. The JSON file was 8.4 MB big, pickle even 11MB. So that made
the problem worse.


## Fuzzy solutions

I'm not sure how to call this right now. "Fuzzy" solutions are ones that work
with probabilities.