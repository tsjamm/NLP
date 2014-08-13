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
primitive_token_detection = re.compile('[^\s=|]+')

# To Extract special tokens like . , ? / and so on...
initials = re.compile('^[\w]\.(\w\.)*',re.U)    # S.P.   or for U.S.A. or e.g.
titles = re.compile('[A-Z]+[a-z]*\.')     # Dr. Mr. Prof.

# non-word character at start or end of token (lower pref compared to about regexps)
#punctuation = re.compile('^\W+|\W+$')
punctuation = re.compile('^[].,<>/?!@#$%&*()~`\'\";:+={}[|\^-]+|[].,<>/?!@#$%&*()~`\'\";:+={}[|\^-]+$') 
single_punct = re.compile('[].,<>/?!@#$%&*()~`\'\";:+={}[|\^-]')

hindi_punct = re.compile(u'[\u0964\u0965]')

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
        initials_obj = re.findall(initials,token)
        #print "initials_obj = ",initials_obj," token = "+token
        titles_obj = re.findall(titles,token)
        #print "titles_obj = ",titles_obj," token = "+token
        punctuation_obj = re.findall(punctuation,token)
        #print "punctuation_obj = ",punctuation_obj," token = "+token
        hindi_punct_obj = re.findall(hindi_punct,token)
        #print "hindi_punct_obj = ",hindi_punct_obj," token = "+token
        
        if hindi_punct_obj:
            for h_punct_token in hindi_punct_obj:
                special_tokens.append(h_punct_token)
                token = re.sub(h_punct_token, "", token)
        
        if (not initials_obj) and (not titles_obj) and (punctuation_obj):
            #print "punc = ",punctuation_obj," token = "+token
            for punct_token in punctuation_obj:
                single_punct_obj = re.findall(single_punct, punct_token)
                if single_punct_obj:
                    special_tokens.extend(single_punct_obj)
                else:
                    special_tokens.append(punct_token)
            #special_tokens.extend(punctuation_obj) #not necessary since above for loop
            special_tokens.append(re.sub(punctuation, "", token))
        else:
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

# This function reads a given file line by line and processes the tokenization
def frequency_from_file(file_path):
    freq_map = {}
    total_freq = 0;
    total_uniques = 0;
    with open(file_path) as input_file:
        for input_line in input_file:
            input_tokens = get_primitive_tokens(input_line)
            input_tokens = get_special_tokens(input_tokens)
            total_freq += len(input_tokens)
            freq_map = get_frequency_map(input_tokens,freq_map)
    total_uniques = len(freq_map)
    #print "Total Number of Tokens : ", total_freq
    #print "Total Number of Uniques : ", total_uniques
    return freq_map

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

# Sample line for testing
#line = "Cats are smarte'r th-an do:gs : : : and this is another test for dogs"
#tokens = get_primitive_tokens(line)
#freq_map = get_frequency_map(tokens)


# Calculating Frequency of Tokens
#freq_map = frequency_from_file("testfile.txt")
#write_to_file("testfile.processed.txt",freq_map)

# For Assignment
freq_map = frequency_from_file("English.txt")
write_to_file("Processed.English.txt",freq_map)
write_top_50_to_file("Processed50.English.txt",freq_map)
freq_map = frequency_from_file("Hindi.txt")
write_to_file("Processed.Hindi.txt",freq_map)
write_top_50_to_file("Processed50.Hindi.txt",freq_map)
freq_map = frequency_from_file("Telugu.txt")
write_to_file("Processed.Telugu.txt",freq_map)
write_top_50_to_file("Processed50.Telugu.txt",freq_map)


exit(0)

