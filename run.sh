#!/bin/sh

# Data folder path
input_data_path=data/input

# Stanford word segmenter path
segmenter_path=lib/stanford-segmenter-2012-11-11

# opencc config file path
opencc_config_file_path=/usr/lib/i386-linux-gnu/opencc/zhtw2zhcn_s.ini

# stopword list path
stopwords_file=data/stopwords.txt

# sentiment lexicon files path
lexicon_files_path=data/NTUSD

# sentence probabilities file path
probabilities_file_path=data/trained_sentence_probabilities

# Output path
output_path=data/output

simplified_ext=.simplified
segmented_ext=.segmented
freq_ext=.word_frequencies
results_ext=.analysis_results


for file in $input_data_path/* ; do
    filename=`basename $file`
    echo '\nProcessing file:' ${filename} '...'
   
    echo '\nConverting text to Simplified Chinese...\n\n'
    # First convert everything into Simplified Chinese
    opencc -i $file -o $output_path/${filename}.simplified -c $opencc_config_file_path
    
    echo '\nSegmenting sentences into word chunks...\n\n'
    # Segment the data
    java -mx2g -cp $segmenter_path/seg.jar edu.stanford.nlp.ie.crf.CRFClassifier \
        -sighanCorporaDict $segmenter_path/data \
        -testFile $output_path/${filename}${simplified_ext} \
        -inputEncoding UTF-8 \
        -outputEncoding UTF-8 \
        -sighanPostProcessing true \
        -keepAllWhitespaces false \
        -loadClassifier $segmenter_path/data/ctb.gz \
        -serDictionary $segmenter_path/data/dict-chris6.ser.gz > $output_path/${filename}${segmented_ext}

    echo '\nAnalyzing sentiments...\n\n'
    python src/sentiment_analyzer.py ${output_path}/${filename}${segmented_ext} ${output_path}/${filename}${results_ext} ${lexicon_files_path}/Positive_simp_UTF8.txt ${lexicon_files_path}/Negtive_simp_UTF8.txt ${probabilities_file_path} 

    echo '\nFinished!\n'

done
