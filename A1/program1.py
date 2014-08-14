#!/usr/bin/python

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Monsoon Semester 2014 NLP Course

# This is a primitive program that parses a given text into tokens
# Using Regular Expressions

import re           # For Regex
import operator     # For Ordering by Value

# To Extract non-space charactered tokens (primitive tokens)
primitive_token_detection = re.compile('[^\s]+')

# To Extract special tokens like . , ? / and so on...
initials = re.compile('^[\w]\.(\w\.)*',re.U)    # S.P.   or for U.S.A. or e.g.
titles = re.compile('[A-Z]+[a-z]*\.')           # Dr. Mr. Prof.
quote_s = re.compile('[^\s]+\'s')               # King's

# non-word character at start or end of token (lower pref compared to above regexps)
#punctuation = re.compile('^\W+|\W+$')
punctuation_string = '[].,<>/?!@#$%&*()~`\'\";:+={}[|\^-]'
punctuation = re.compile('^'+punctuation_string+'+|'+punctuation_string+'+$') 
punctuation_start = re.compile('^'+punctuation_string+'+') 
punctuation_end = re.compile(punctuation_string+'+$') 
# detecting punctuation anywhere...
single_punct = re.compile('('+punctuation_string+')')

hindi_punct = re.compile(u'[\u0964\u0965]')

hyphenation = re.compile("\w+-\w+(-\w+)*")                  # state-of-the-art
numbers = re.compile("\d+|\d+[:.]\d+(\.\d+)*\w*|\d+\w*")    # 4, 3:15, 192.168.2.1, 9.8ms, 34th
dates = re.compile("\d+[.-/]\d+[.-/]\d+")                   # 21-12-14, 7-12-2020, 3.03.43
url = re.compile("^http://|^https://|^ftp://|^file:///")    # urls starting with these



# This function returns the primitive non space tokens
# in the given input string
def get_primitive_tokens(text):
    list_obj = re.findall(primitive_token_detection,text)
    if list_obj:
        #for i in listObj:
            #print i
        return list_obj
    else:
        #print "no primitive tokens detected for line : "+text
        return []

# This function checks certain special tokens like punctuation marks and so on
def get_special_tokens(token_list):
    special_tokens = []
    for token in token_list:
        punctuation_obj = re.findall(single_punct,token)
        #print "punctuation_obj = ",punctuation_obj," token = "+token
        hindi_punct_obj = re.findall(hindi_punct,token)
        #print "hindi_punct_obj = ",hindi_punct_obj," token = "+token
        
        if punctuation_obj:
            initials_obj = re.findall(initials,token)
            titles_obj = re.findall(titles,token)
            url_obj = re.findall(url,token)
            punct_start_obj = re.findall(punctuation_start,token)
            punct_end_obj = re.findall(punctuation_end,token)
            
            if (not initials_obj) and (not titles_obj) and (not url_obj):
                for punct_token in punct_start_obj:
                    single_punct_obj = re.findall(single_punct, punct_token)
                    if single_punct_obj:
                        special_tokens.extend(single_punct_obj)
                    else:
                        special_tokens.append(punct_token)
                        
                center_token = re.sub(punctuation, "", token)
                quote_s_obj = re.findall(quote_s,center_token)
                hyphen_obj = re.findall(hyphenation,center_token)
                number_obj = re.findall(numbers,center_token)
                date_obj = re.findall(dates,center_token)
                token_split_obj = re.split(single_punct, center_token)
                if (not quote_s_obj) and (not hyphen_obj) and (not number_obj) and (not date_obj) and (token_split_obj):
                    special_tokens.extend(token_split_obj)
                else:
                    special_tokens.append(center_token)
                
                for punct_token in punct_end_obj:
                    single_punct_obj = re.findall(single_punct, punct_token)
                    if single_punct_obj:
                        special_tokens.extend(single_punct_obj)
                    else:
                        special_tokens.append(punct_token)
        if hindi_punct_obj:
            for h_punct_token in hindi_punct_obj:
                special_tokens.append(h_punct_token)
                token = re.sub(h_punct_token, "", token)
                
        if (not punctuation_obj) and (not hindi_punct_obj):
            special_tokens.append(token)

    return special_tokens
            

# This function returns a list of sorted tuples
def get_sorted_tuples(freq_map):
    sorted_tuples = sorted(freq_map.iteritems(), key=operator.itemgetter(1))
    return sorted_tuples

# This function returns a frequency dictionary of the given list
def get_frequency_map(token_list, frequency_map = {}):
    for i in token_list:
        if i=='':
            continue
        if frequency_map.get(i,None):
            frequency_map[i] += 1
        else:
            frequency_map[i] = 1 
    return frequency_map

# This function writes the freq_map to file as sorted tuples
def write_to_file(file_path,freq_map):
    total_freq = 0;
    total_uniques = 0;
    sorted_tuples = get_sorted_tuples(freq_map)
    sorted_tuples.reverse()
    with open(file_path,'w') as output_file:
        for pair in sorted_tuples:
            output_file.write("{0}\t{1}\n".format(pair[0],pair[1]))
            total_freq += pair[1]
            total_uniques += 1
        output_file.write("Total Number of Tokens : {0}\n".format(total_freq))
        output_file.write("Total Number of Uniques : {0}\n".format(total_uniques))
    print "Finished writing to File : "+file_path
    print "Total Number of Tokens : {0}".format(total_freq)
    print "Total Number of Uniques : {0}\n".format(total_uniques)

# This function writes the freq_map to file as sorted tuples
def write_rank_to_file(file_path,freq_map):
    total_count = 1;
    sorted_tuples = get_sorted_tuples(freq_map)
    sorted_tuples.reverse()
    with open(file_path,'w') as output_file:
        for pair in sorted_tuples:
            output_file.write("{0},{1}\n".format(total_count,pair[1]))
            total_count += 1
    print "Finished writing to File : "+file_path
    print "Total Number of lines : {0}".format(total_count)

# This function takes the top 50 unique tokens and writes to file
def write_top_50_to_file(file_path,freq_map):
    total_freq = 0;
    total_uniques = 0;
    sorted_tuples = get_sorted_tuples(freq_map)
    sorted_tuples.reverse()
    with open(file_path,'w') as output_file:
        for pair in sorted_tuples:
            output_file.write("{0}\t{1}\n".format(pair[0],pair[1]))
            total_freq += pair[1]
            total_uniques += 1
            if(total_uniques>=50):
                break
        output_file.write("Total Number of Tokens : {0}\n".format(total_freq))
        output_file.write("Taken Top {0}\n".format(total_uniques))
    print "Finished writing to File : "+file_path
    print "Total Number of Tokens : {0}".format(total_freq)
    print "Written to File Top {0}\n".format(total_uniques)

# ngram Generation from unigrams
def get_n_grams(n, unigrams):
    ngrams = []
    list_len = len(unigrams)
    if list_len >= n :
        start = 0
        end = list_len+1
        for index in range(start,end):
            if index <= (end/n):
                sub_words_list = unigrams[index:index+n]
                ngram_sequence = ' '.join(sub_words_list)
                ngrams.append(ngram_sequence)
    return ngrams
        

# Writing a List to File
def write_list_to_file(file_path, input_list):
    total_count = 0
    with open(file_path,'w') as output_file:
        for line in input_list:
            output_file.write(line+"\n")
            total_count += 1
        output_file.write("Total Number of Tokens : {0}\n".format(total_count))
    print "Finished writing to File : "+file_path
    print "Total Number of Tokens : {0}\n".format(total_count)

# This function reads a given file line by line and processes the tokenization
def process_file(file_path):
    freq_map = {}
    unigrams = []
    freq_map_b = {}
    bigrams = []
    freq_map_t = {}
    trigrams = []
    total_freq = 0;
    total_uniques = 0;
    with open(file_path) as input_file:
        for input_line in input_file:
            input_tokens = get_primitive_tokens(input_line)
            input_tokens = get_special_tokens(input_tokens)
            unigrams.extend(input_tokens)
            input_bigrams = get_n_grams(2, input_tokens)
            bigrams.extend(input_bigrams)
            input_trigrams = get_n_grams(3, input_tokens)
            trigrams.extend(input_trigrams)
            total_freq += len(input_tokens)
            freq_map = get_frequency_map(input_tokens,freq_map)
            freq_map_b = get_frequency_map(input_bigrams,freq_map_b)
            freq_map_t = get_frequency_map(input_trigrams,freq_map_t)
    total_uniques = len(freq_map)
    write_to_file("Processed.Frequency.Unigrams."+file_path,freq_map)
    write_to_file("Processed.Frequency.Bigrams."+file_path,freq_map_b)
    write_to_file("Processed.Frequency.Trigrams."+file_path,freq_map_t)
    write_top_50_to_file("Processed.Top50."+file_path,freq_map)
    write_list_to_file("Processed.Unigrams."+file_path,unigrams)
    write_list_to_file("Processed.Bigrams."+file_path,bigrams)
    write_list_to_file("Processed.Trigrams."+file_path,trigrams)
    write_rank_to_file("Processed.Ranks.Unigrams."+file_path,freq_map)
    write_rank_to_file("Processed.Ranks.Bigrams."+file_path,freq_map_b)
    write_rank_to_file("Processed.Ranks.Trigrams."+file_path,freq_map_t)

# Sample line for testing
#line = "Cats are smarte's th-an do:gs : : : and this is another test for dogs"
#tokens = get_primitive_tokens(line)
#tokens = get_special_tokens(tokens)
#print tokens
#freq_map = get_frequency_map(tokens)

# Calculating Frequency of Tokens
#freq_map = frequency_from_file("testfile.txt")
#write_to_file("testfile.processed.txt",freq_map)
#process_file("testfile.txt")

# For Assignment
process_file("English.txt")
process_file("Hindi.txt")
process_file("Telugu.txt")


exit(0)

