#!/usr/bin/python

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Monsoon Semester 2014 NLP Course

# program 3 - Smoothing and language modeling

import nlpfunc
import time

print "Runnning Program 3...."
starttime = time.asctime( time.localtime(time.time()) )
print "Start Time :", starttime


def process_file(file_path,file_name):
    if (not file_name) or file_name=="":
        file_name="default";
        
    freq_map = {}
    unigrams = []
    freq_map_b = {}
    bigrams = []
    freq_map_t = {}
    trigrams = []
    with open(file_path) as input_file:
        for input_line_raw in input_file:
            input_line = unicode(input_line_raw,"utf-8")
            #Getting Unigrams
            input_tokens = nlpfunc.get_primitive_tokens(input_line)
            input_tokens = nlpfunc.get_special_tokens(input_tokens)
            unigrams.extend(input_tokens)
            #Getting Bigrams
            input_bigrams = nlpfunc.get_n_grams(2, input_tokens)
            bigrams.extend(input_bigrams)
            #Getting Trigrams
            input_trigrams = nlpfunc.get_n_grams(3, input_tokens)
            trigrams.extend(input_trigrams)
            #Getting Frequency Maps
            freq_map = nlpfunc.get_frequency_map(input_tokens,freq_map)
            freq_map_b = nlpfunc.get_frequency_map(input_bigrams,freq_map_b)
            freq_map_t = nlpfunc.get_frequency_map(input_trigrams,freq_map_t)
    

#For Assignment
process_file("../Datasets/Toy_Data.txt", "ToyData")


endtime = time.asctime( time.localtime(time.time()) )
print "Start Time :", starttime
print "End Time :", endtime

exit(0)