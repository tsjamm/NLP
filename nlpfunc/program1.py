#!/usr/bin/python

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Monsoon Semester 2014 NLP Course

# This is a primitive program that parses a given text into tokens
# Using Regular Expressions

import nlpfunc
import os.path

print "Runnning Program 1...."

# Sample line for testing
#line = "Cats are smarte's th-an do:gs : : : and this is another test for dogs"
#tokens = nlpfunc.get_primitive_tokens(line)
#tokens = nlpfunc.get_special_tokens(tokens)
#print tokens
#freq_map = nlpfunc.get_frequency_map(tokens)

# Calculating Frequency of Tokens
#freq_map = nlpfunc.frequency_from_file("testfile.txt")
#nlpfunc.write_to_file("testfile.processed.txt",freq_map)
#nlpfunc.process_file("testfile.txt")

# This function reads a given file line by line and processes the tokenization
def process_file(file_path,file_name):
    if (not file_name) or file_name=="":
        file_name="default";
    freq_map = {}
    unigrams = []
    freq_map_b = {}
    bigrams = []
    freq_map_t = {}
    trigrams = []
    total_freq = 0;
    with open(file_path) as input_file:
        for input_line_raw in input_file:
            input_line = unicode(input_line_raw,"utf-8")
            input_tokens = nlpfunc.get_primitive_tokens(input_line)
            input_tokens = nlpfunc.get_special_tokens(input_tokens)
            unigrams.extend(input_tokens)
            input_bigrams = nlpfunc.get_n_grams(2, input_tokens)
            bigrams.extend(input_bigrams)
            input_trigrams = nlpfunc.get_n_grams(3, input_tokens)
            trigrams.extend(input_trigrams)
            total_freq += len(input_tokens)
            freq_map = nlpfunc.get_frequency_map(input_tokens,freq_map)
            freq_map_b = nlpfunc.get_frequency_map(input_bigrams,freq_map_b)
            freq_map_t = nlpfunc.get_frequency_map(input_trigrams,freq_map_t)
    d = os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/"
    if not os.path.exists(d):
        os.makedirs(d)
    nlpfunc.write_freq_map_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.Frequency.Unigrams."+file_name,freq_map)
    nlpfunc.write_freq_map_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.Frequency.Bigrams."+file_name,freq_map_b)
    nlpfunc.write_freq_map_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.Frequency.Trigrams."+file_name,freq_map_t)
    nlpfunc.write_top_n_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.200TopUnigrams."+file_name,freq_map,200)
    nlpfunc.write_last_n_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.200LastUnigrams."+file_name,freq_map,200)
    nlpfunc.write_middle_n_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.200MiddleUnigrams."+file_name,freq_map,200)
    nlpfunc.write_top_n_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.200TopBigrams."+file_name,freq_map_b,200)
    nlpfunc.write_last_n_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.200LastBigrams."+file_name,freq_map_b,200)
    nlpfunc.write_middle_n_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.200MiddleBigrams."+file_name,freq_map_b,200)
    nlpfunc.write_top_n_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.200TopTrigrams."+file_name,freq_map_t,200)
    nlpfunc.write_last_n_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.200LastTrigrams."+file_name,freq_map_t,200)
    nlpfunc.write_middle_n_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.200MiddleTrigrams."+file_name,freq_map_t,200)
    nlpfunc.write_list_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.Unigrams."+file_name,unigrams)
    nlpfunc.write_list_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.Bigrams."+file_name,bigrams)
    nlpfunc.write_list_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.Trigrams."+file_name,trigrams)
    nlpfunc.write_rank_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.Ranks.Unigrams."+file_name,freq_map)
    nlpfunc.write_rank_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.Ranks.Bigrams."+file_name,freq_map_b)
    nlpfunc.write_rank_to_file(os.path.dirname(__file__) +"/../Results/A1/"+file_name+"/Processed.Ranks.Trigrams."+file_name,freq_map_t)


# For Assignment
process_file("../Datasets/English.txt","English")
process_file("../Datasets/Hindi.txt","Hindi")
process_file("../Datasets/Telugu.txt","Telugu")
process_file("../Datasets/Toy_Data.txt","ToyData")

exit(0)

