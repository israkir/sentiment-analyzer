#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------------------------------------------
#
# Program Name          : sentiment_analyzer.py
# Authors               : W.B.Lee, H.C.Lee, Y.K.Wang, T.T.Mutlugun, H.C.Kirmizi
# Date                  : December 30, 2012
# Description           : Analyze 
# Running command       : python sentiment_analyzer.py [in-file] [out-file] [pos-lexicons-file] [neg-lexicons-file]
# Python version        : Python 2.7.1
#
# --------------------------------------------------------------------------------------------------------------------

import sys
import codecs


def train_sentiment_lexicons(pos_lexicons_filename, neg_lexicons_filename):
    '''
    Assigns the sentiment polarity for each lexicons.
    Returns positive lexicons and negative lexicons in dictionary format.
    '''
    pos_file = codecs.open(pos_lexicons_filename, 'r', 'utf-8')
    neg_file = codecs.open(neg_lexicons_filename, 'r', 'utf-8')

    pos_lexicons = []
    for i in range(9365):
        s = pos_file.readline().strip()
        pos_lexicons.append(s)

    neg_lexicons = []
    for i in range(11230):
        s = neg_file.readline().strip()
        neg_lexicons.append(s)

    pos_file.close()
    neg_file.close()

    return pos_lexicons, neg_lexicons


def filter_punctuation(text):
    punctuations = u"。「」.・,﹁﹂“”、·《》—～；：？——!！\"%$'&)(+*-/.;:=<?>@[]\\_^`{}|~\#"
    translate_table = dict((ord(char), None) for char in punctuations)
    
    return text.translate(translate_table)


def analyze_sentence_sentiment(input_filename, output_filename, pos_lexicons, neg_lexicons, probability_filename):
    '''
    Analyzes the input file in given format and writes the
    analysis results to an output file.

    Basic algorithm:
    ----------------

    Initialize a score for each clause. 
    For each word segment in clause:
        If word segment is a positive lexicon, then score++
        If word segment is a negative lexicon, then score--
    If score > 0, then clause polarity is 1.
    If score < 0, then clause polarity is -1,
    If score = 0, then clause polarity is 0.
    
    '''
    input_file = codecs.open(input_filename, 'r', 'utf-8')
    output_file = codecs.open(output_filename, 'w', 'utf-8')
    
    total_sentences = input_file.readline().strip()

    # retrieve the probability model
    tem_dict, con_dict, com_dict, exp_dict = retrieve_probability_model(probability_filename)

    p1 = ''
    p2 = ''

    for i in range(3 * int(total_sentences)):
        line = input_file.readline().strip('\n')
        line = filter_punctuation(line)

        # write the score for whole sentences
        if (i % 3) == 2:
            p3 = getAllPolarity(p1, p2, line, tem_dict, con_dict, com_dict, exp_dict)
            output_file.write(unicode(p3, 'utf-8') + u'\n')
        
        # analyze each clause in the sentence
        else:
            score = 0
            token = ''
            for word in line.split():
                if word in pos_lexicons:
                    #print 'pos found: %s' % word
                    score += 1
                elif word in neg_lexicons:
                    #print 'neg found: %s' % word
                    score -= 1
                
            if score > 0:
                output_file.write(u'1\n')
                token = '+'
            elif score < 0:
                output_file.write(u'-1\n')
                token = '-'
            else:
                output_file.write(u'0\n')
                token = 'x'

            if (i % 3) == 0:
                p1 = token
            elif (i % 3) == 1:
                p2 = token
                
    input_file.close()
    output_file.close()


def retrieve_probability_model(probability_filename):
    prob_file = codecs.open(probability_filename, 'r', 'utf8')

    tem = {}
    con = {}
    com = {}
    exp = {}

    if prob_file.readline().strip() == "Temporal":
        for i in range(27):
            polarity = prob_file.readline().strip();
            probability = prob_file.readline().strip();
            tem[polarity] = probability;
            #print 'tem['+polarity+']:'+str(probability)

    if prob_file.readline().strip() == "Contingency":
        for i in range(27):
            polarity = prob_file.readline().strip();
            probability = prob_file.readline().strip();
            con[polarity] = probability;
            #print 'con['+polarity+']:'+str(probability)

    if prob_file.readline().strip() == "Comparison":
        for i in range(27):
            polarity = prob_file.readline().strip();
            probability = prob_file.readline().strip();
            com[polarity] = probability;
            #print 'com['+polarity+']:'+str(probability)

    if prob_file.readline().strip() == "Expansion":
        for i in range(27):
            polarity = prob_file.readline().strip();
            probability = prob_file.readline().strip();
            exp[polarity] = probability;
            #print 'exp['+polarity+']:'+str(probability)

    prob_file.close()

    return tem, con, com, exp


def getAllPolarity(p1, p2, relation, tem_dict, con_dict, com_dict, exp_dict):
    relArray = {}

    if relation == "Temporal":
        relArray = tem_dict
    elif relation == "Contingency":
        relArray = con_dict
    elif relation == "Comparison":
        relArray = com_dict
    elif relation == "Expansion":
        relArray = exp_dict

    polarArray = ['+', 'x', '-']
    rToken = '+'
    probValue = 0
    for p3 in polarArray:
        polarity = p1+p2+p3
        if relArray[polarity] > probValue:
            probValue = relArray[polarity]
            rToken = p3

    if rToken == "+":
        return "1"
    elif rToken == "x":
        return "0"
    elif rToken == "-":
        return "-1"


def main():
    '''
    Main procedure drives the whole analysis process.
    '''
    input_filepath = sys.argv[1]
    output_filepath = sys.argv[2]
    positive_lexicons_filepath = sys.argv[3]
    negative_lexicons_filepath = sys.argv[4]
    probability_filepath = sys.argv[5]

    print 'Training positive and negative sentiment lexicons...'
    pos_lexicons, neg_lexicons = train_sentiment_lexicons(positive_lexicons_filepath, negative_lexicons_filepath)

    print 'Analyzing sentence sentiments from the input file...'
    analyze_sentence_sentiment(input_filepath, output_filepath, pos_lexicons, neg_lexicons, probability_filepath)


if __name__ == '__main__':
    main()
