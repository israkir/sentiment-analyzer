Description
===========

This project aims to implement sentiment orientation analyzer for discourse relation pairs.


Dependencies
============

1. `opencc` package (v0.3.0) for Simplified-Traditional Chinese conversion.
2. `stanford-segmenter` package (2012-11-11) for segmenting Simplified Chinese sentences.

Note: `stanford-segmenter` is included in `lib/` directory. It is suggested to install `opencc` via your linux distribution package manager.


Instructions
============

1. Make sure `opencc_config_file_path` is set to correct path (different linux distributions may have different paths) in `run.sh`. Currenty it is set to:
    
    `opencc_config_file_path=/usr/lib/i386-linux-gnu/opencc/zhtw2zhcn_s.ini`

2. Put your input file into `data/input/` folder.


Notes
=====

1. Assuming your input file name is `dev.in`, these files will be generated in order in `data/output/` directory:

  * `dev.in.simplified`: Simplified Chinese version of `dev.in`.
  
  * `dev.in.segmented`: Word segmented version of `dev.in.simplified`.
  
  * `dev.in.analysis_results`: All sentiment analysis results computed from `dev.in.segmented` with punctuations cleaned.

2. There is a file `data/trained_sentence_probabilities`  which contains the sentence probabilities for different clause relations trained from the `dev.in` and its correct output. It must be one of inputs of `src/sentiment_analyzer/py` which is set in `run.sh`.

3. There is a stopwords list included in `data/stopwords.txt` which are not used in the current codebase. It might be used for larger input data to improve performance later in the future.


Input Format
============


The first line is a positive integer `N` denoting the number of two-clause sentences. 

The following `3xN` lines are given.

Of each sentence, the first line is the first clause, and the second line is the second clause. The third line indicates the relation type between these two clauses.

Sample
------

    3
    他很年輕，
    但已經是世界上最棒的足球運動員之一。
    Comparison
    回答這個問題很容易，
    解決卻很難。
    Comparison
    尤卡旦島的馬雅山地
    曾是印第安文化的發源地。
    Expansion


Output Format
=============

For each sentence, output contains 3 numbers in separate lines.

Sentiment polarity of the first clause
Sentiment polarity of the second clause
Sentiment polarity of the whole sentence

`-1` denotes `negative polarity`, `0` denotes `neutral polarity`, and `1` denotes `positive polarity`.

Sample
------

    -1
    1
    1
    1
    -1
    -1
    0
    0
    0
