#!/usr/bin/python

import random
import re
import sys

WORDS = {}

def isint(t):
    try:
        i = int(t)
    except:
        return False
    return True

def pull_verses():

    with open('bible.txt') as f:
        raw = f.read()


    # numbers:numbers followed by as many not-numbers as possible
    pattern = '\d+:\d+[^\d]*'

    M = re.findall(pattern,raw)

    verses = [' '.join(m.split()[1:]) for m in M]
    
    #for i in range(200):
    #    print ' '.join(M[i].split()[1:])
    #    print

    #print len(verses) #(outputs 31102)
    """
    There are 23,145 verses in the Old Testament and 7,957 verses in the New Testament. This gives a total of 31,102 verses, which is an average of a little more than 26 verses per chapter. Contrary to popular belief, Psalm 118 does not contain the middle verse of the Bible.
    """
    return verses

def clean(verse):
    alphabet = "abcdefghijklmnopqrstuvwxyz "
    v = verse.lower()
    return filter(lambda x: x in alphabet, v)

def populate():
    global WORDS
    raw_verses = pull_verses()

    verses = [clean(verse) for verse in raw_verses]
    
    #for i in range(30):
    #    print verses[i]

    for verse in verses:
        spl = verse.split()
        for ind,word in enumerate(spl[:-1]):
            if WORDS.has_key(word):
                WORDS[word].append(spl[ind+1])
            else:
                WORDS[word] = [spl[ind+1]]

def make_markov_sentence(length, seed=None):
    if not seed:
        R = random.randint(0,len(WORDS)-1)
        seed = WORDS.keys()[R]
    if not WORDS.has_key(seed):
        sys.stderr.write("Word not found: " + seed + "\n")
        sys.exit(1)

    sentence = [seed]
    last = seed
    for i in range(length-1):
        pool = WORDS[last]
        r = random.randint(0,len(pool)-1)
        last = pool[r]
        sentence.append(last)
    return ' '.join(sentence)

def make_rho_sentence(length, seed=None):
    if not seed:
        R = random.randint(0,len(WORDS)-1)
        seed = WORDS.keys()[R]
    if not WORDS.has_key(seed):
        sys.stderr.write("Word not found: " + seed + "\n")
        sys.exit(1)

    sentence = [seed]
    last = seed
    for i in range(length-1):
        pool = WORDS[last]
        last = most_common_word(pool)
        sentence.append(last)
    main,loop = format_rho(sentence)

    return ' '.join(main) + ' (' + ' '.join(loop) + ')'

def format_rho(some_list):
    count = 0
    index = 0
    while count < 2:
        if index == len(some_list):
            return some_list,[]
        count = some_list.count(some_list[index])
        index += 1
    index -= 1
    word = some_list[index]
    i = some_list.index(word)
    j = some_list[i+1:].index(word) + i

    return some_list[:i],  some_list[i:j+1]

    

def make_canonical_sentence(length, seed=None):
    if not seed:
        R = random.randint(0,len(WORDS)-1)
        seed = WORDS.keys()[R]
    if not WORDS.has_key(seed):
        sys.stderr.write("Word not found: " + seed + "\n")
        sys.exit(1)

    sentence = [seed]
    last = seed
    for i in range(length-1):
        pool = WORDS[last]
        pool = filter(lambda x: x not in sentence, pool)
        last = most_common_word(pool)
        sentence.append(last)
    return ' '.join(sentence)

def most_common_word(some_list):
    count = {}
    for word in some_list:
        count[word] = count[word] + 1 if count.has_key(word) else 1
    pairs = [(count[key], key) for key in count.keys()]

    # Ascending sort
    pairs.sort()
    return pairs[-1][1]


if __name__ == '__main__':
    populate()
    #while 1:
    #    print make_markov_sentence(10, seed='the')
    for i in range(10):
        print make_rho_sentence(30)
    print make_canonical_sentence(20)




