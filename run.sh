#!/bin/sh

# Data folder path
input_data_path=data/input

# Stanford word segmenter path
segmenter_path=lib/stanford-segmenter-2012-11-11

# Stanford POS tagger path
pos_tagger_path=lib/stanford-postagger-full-2012-11-11

# opencc config file path
opencc_config_file_path=/usr/lib/i386-linux-gnu/opencc/zhtw2zhcn_s.ini

# stopword list path
stopwords_file=data/stopwords.txt

# Output path
output_path=data/output

simplified_ext=.simplified
segmented_ext=.segmented
postag_ext=.pos_tagged
cleaned_ext=.stopwords_cleaned
freq_ext=.word_frequencies


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

    echo '\nPOS tagging the words...\n\n'
    java -mx2g -cp $pos_tagger_path/stanford-postagger.jar: edu.stanford.nlp.tagger.maxent.MaxentTagger \
        -model $pos_tagger_path/models/chinese-distsim.tagger \
        -outputFormat slashTags -tagSeparator \_ \
        -textFile $output_path/${filename}${segmented_ext} > $output_path/${filename}${postag_ext}

    echo '\nCleaning stopwords...\n\n'
    # Clean stopwords
    python $output_path/${filename}${segmented_ext} $stopwords_file $output_path/${filename}${cleaned_ext} $output_path/${filename}${freq_ext}

done
