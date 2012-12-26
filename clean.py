# coding: utf-8
# -----------------------------------------------------------------------
#
# Program Name          : clean.py
# Author                : Tahsin Türker Mutlugün, modified version of segmentator.py
# Date                  : December 23, 2012
# Description           : Filter punctuations and words that are unnecessary for sentiment analysis
#                         from a given text file
# Running command       : python clean.py [input-file] [stopwords-file] [optional output-file] [optional word-frequency-output-file]
# Python version        : Python 2.7.1
#
# -----------------------------------------------------------------------
import codecs, sys, string, copy
from collections import Counter, OrderedDict


# Input functions
def read_file(filename):
    try:
        file = codecs.open(filename,'r','utf8')
    except IOError:
        print "\"%s\" no such file exists." % filename
        return None
        
    ret = file.read()
    file.close()
    return ret

def read_file_into_list(filename):
    try:
        file = codecs.open(filename, 'r', 'utf8')
    except IOError:
        print "\"%s\" no such file exists." % filename
        return None

    ret = [line.strip() for line in file]
    file.close()
    return ret

# Output functions
def print_unicode(text):
    print unicode(text).encode('utf8')

def write_to_file(filename, text):
    f = codecs.open(filename, 'w', 'utf8')
    f.write(text)
    f.close()

def write_frequencies(filename, freq_list):
    f = codecs.open(filename, 'w', 'utf8')
    d = OrderedDict(sorted(freq_list.items(), key=lambda t:t[1], reverse=True))
    f.write('Character\tFrequency\n')
    f.write('---------------------\n')
    for key, val in d.items():
        f.write('  %s \t\t  %d\n' % (key, val))
    f.close()
    
# Filtering functions
def filter_punctuation(text):
    punctuations = u"。「」.,﹁﹂“”、·《》—～；？——!！\"%$'&)(+*-/.;:=<?>@[]\\_^`{}|~\#"
    translate_table = dict((ord(char), None) for char in punctuations)
    
    return text.translate(translate_table)

def filter_stopwords(stopword_list, text):
    for char in stopword_list:
        text = text.replace(char, '')
    
    return text
    
# Miscellaneous functions    
def list_word_frequency(text):
    text_untagged = copy.deepcopy(text)
    tags = [u'Comparison', u'Contingency', u'Expansion', u'Temporal']
    for tag in tags:
        text_untagged = text_untagged.replace(tag, '')
    cnt = Counter()
    for word in text_untagged:
        if (('\n' not in word) and (' ' not in word)):
            cnt[word] += 1

    return cnt
    
    
def main():
    if (len(sys.argv) < 3):
        print "Usage: python clean.py [input_file] [stopword_list] [[optional] output_file] [[optional] word_freq_output]"
        exit()
        
    if(len(sys.argv) == 3):
        input_file_name = sys.argv[1]
        stopword_file_name = sys.argv[2]
        output_file_name = input_file_name + '.filtered'
        word_freq_output = None
    elif(len(sys.argv) == 4):
        input_file_name = sys.argv[1]
        stopword_file_name = sys.argv[2]
        output_file_name = sys.argv[3]
        word_freq_output = None
    elif(len(sys.argv) == 5):
        input_file_name = sys.argv[1]
        stopword_file_name = sys.argv[2]
        output_file_name = sys.argv[3]
        word_freq_output = sys.argv[4]
        
    test_data_text = read_file(input_file_name)
    if(test_data_text is None):
        print_unicode("Exiting cleaner due to errors.")
        exit()
    stopword_list = read_file_into_list(stopword_file_name)
    if(stopword_list is None):
        print_unicode("Exiting cleaner due to errors.")
        exit()

    #Filter out punctuation
    clean_test_data_text = filter_punctuation(test_data_text)
    
    #Get frequency of words
    if(word_freq_output is not None):
        word_freq = list_word_frequency(clean_test_data_text)
        write_frequencies(word_freq_output, word_freq)
    
    #Filter out stopwords
    clean_test_data_text = filter_stopwords(stopword_list, clean_test_data_text)
    
    write_to_file(output_file_name, clean_test_data_text)
    
    
if __name__ == '__main__':
    main()