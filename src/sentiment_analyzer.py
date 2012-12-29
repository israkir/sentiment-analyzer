# -*- coding: utf-8 -*-
#!/usr/bin/env python

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
    pos_lexicons = {}
    neg_lexicons = {}

    pos_file = codecs.open(pos_lexicons_filename, 'r', 'utf8')
    neg_file = codecs.open(neg_lexicons_filename, 'r', 'utf8')

    for i in range(9365):
        s = pos_file.readline().strip('\n').encode('utf-8')
        pos_lexicons[s] = 1

    for i in range(11230):
        s = neg_file.readline().strip('\n').encode('utf-8')
        neg_lexicons[s] = -1

    pos_file.close()
    neg_file.close()

    return pos_lexicons, neg_lexicons


def analyze_sentence_sentiment(input_filename, output_filename, pos_lexicons, neg_lexicons):
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
    
    TODO: Hung-Chi: Explain sentence polarity part here!
    '''
    input_file = codecs.open(input_filename, 'r', 'utf8')
    output_file = codecs.open(output_filename, 'w', 'utf8')

    total_sentences = input_file.readline().strip()
    output_file.write(total_sentences + '\n')

    for i in range(3 * int(total_sentences)):
        line = input_file.readline().strip('\n')

        # TODO: Hung-Chi: write the score for whole sentences
        if (i % 3) == 2:
            # temporarily write the relation (line = Expansion etc..)
            output_file.write(line + '\n')
        
        # analyze each clause in the sentence
        else:
            score = 0
            for word in line.split():
                if word in pos_lexicons:
                    #print 'pos found: %s' % word
                    score += 1
                elif word in neg_lexicons:
                    #print 'neg found: %s' % word
                    score -= 1
            
            if score > 0:
                output_file.write('1\n')
            elif score < 0:
                output_file.write('-1\n')
            else:
                output_file.write('0\n')
                
    input_file.close()
    output_file.close()


def main():
    '''
    Main procedure drives the whole analysis process.
    '''
    input_filepath = sys.argv[1]
    output_filepath = sys.argv[2]
    positive_lexicons_filepath = sys.argv[3]
    negative_lexicons_filepath = sys.argv[4]
    
    print 'Training positive and negative sentiment lexicons...'
    pos_lexicons_dict, neg_lexicons_dict = train_sentiment_lexicons(positive_lexicons_filepath, negative_lexicons_filepath)

    print 'Analyzing sentence sentiments from the input file...'
    analyze_sentence_sentiment(input_filepath, output_filepath, pos_lexicons_dict, neg_lexicons_dict)


if __name__ == '__main__':
    main()
