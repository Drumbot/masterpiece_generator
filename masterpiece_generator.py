#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Hugo Mailhot'

"""
This a pretty naive language model trainer. No smoothing, it's just good at recreating part
of what it saw. Still, it's pretty fun. I tested it on a Cannibal Corpse lyrics dataset;
mindless violence ensued!
"""

import codecs
import sys
import re
import getopt
import random


def model_trainer(corpus):
    trigram_count = {}  # Pour unigrammes, n = 1, bigrammes, n = 2, trigrammes, n = 3, etc.
    bigram_count = {}  # Fréquence des (n-1)-grams
    ngram_model = {}
    
    for i in range(len(corpus)-2):
        if tuple(corpus[i:i+3]) in trigram_count:
            trigram_count[tuple(corpus[i:i+3])] += 1
        else:
            trigram_count[tuple(corpus[i:i+3])] = 1

    for i in range(len(corpus)-1):
        if tuple(corpus[i:i+2]) in bigram_count:
            bigram_count[tuple(corpus[i:i+2])] += 1
        else:
            bigram_count[tuple(corpus[i:i+2])] = 1

    for k in trigram_count.keys():
        ngram_model[k] = float(trigram_count[k]) / float(bigram_count[(k[0], k[1])])

    return ngram_model


def generate_masterpiece(length, modele):
    masterpiece = []
    masterpiece += list(random.choice(modele.keys()))

    while (len(masterpiece)) < length:
        context = masterpiece[-2:]
        candidats = [x for x in modele.keys() if x[0]+x[1] == context[0]+context[1]]
        r = random.uniform(0, 1)
        upto = 0
        winner = ''

        for candidat in candidats:
            if upto + modele[candidat] > r:
                winner = candidat
                break
            upto += modele[candidat]

        masterpiece.append(str(winner[2]))
    return masterpiece


def arg_getter(argv):
    inputfile = ''
    outputfile = ''
    length = 0
    try:
        opts, arg = getopt.getopt(argv, "hl:i:o:", ["length=", "ifile=", "ofile="])
    except getopt.GetoptError:
        print 'masterpiece_generator.py -l <length> -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'masterpiece_generator.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ('-l', '--length'):
            length = int(arg)
        elif opt in ("-i", '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg

    return length, inputfile, outputfile


def main(argv):
    length, inputfile, outputfile = arg_getter(argv)
    input_handle = codecs.open(inputfile, 'r', encoding='utf-8')
    raw_training_corpus = input_handle.read()
    input_handle.close()

    split_training_corpus = re.split(r'\W+', raw_training_corpus.lower())
    ngram_model = model_trainer(split_training_corpus)
    masterpiece = generate_masterpiece(length, ngram_model)

    output_handle = codecs.open(outputfile, 'w', encoding='utf-8')
    output_handle.write(' '.join(masterpiece))
    output_handle.close()


if __name__ == "__main__":
    main(sys.argv[1:])