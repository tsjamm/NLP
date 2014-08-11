#!/usr/bin/python

# This is a primitive program that parses a given text into tokens
# Using Regular Expressions

import re           # For Regex
import operator     # For Ordering by Value

# To Extract non-space charactered tokens (primitive tokens)
primitive_token_detection = re.compile('[^\s]+')

# To Extract special tokens like . , ? / and so on...
initials = re.compile('^[\w]\.(\w\.)*')    # S.P.   or for U.S.A. or e.g.
titles = re.compile('[A-Z]+[a-z]*\.')     # Dr. Mr. Prof.

# non-word character at start or end of token (lower pref compared to about regexps)
punctuation = re.compile('^\W*|\W*$')     

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
        titles_obj = re.findall(titles,token)
        punctuation_obj = re.findall(punctuation,token)
        if (not initials_obj) and (not titles_obj) and (punctuation_obj):
            #print "punc = ",punctuation_obj," token = "+token
            punc_obj_noempty=[]
            for p in punctuation_obj:
                if p=='':
                    continue
                else:
                    punc_obj_noempty.append(p)
            print "punc_noempty = ",punc_obj_noempty," token = "+token
            special_tokens.extend(punc_obj_noempty)
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
    with open(file_path) as input_file:
        for input_line in input_file:
            input_tokens = get_primitive_tokens(input_line)
            input_tokens = get_special_tokens(input_tokens)
            freq_map = get_frequency_map(input_tokens,freq_map)
    return freq_map

# Sample line for testing
#line = "Cats are smarte'r th-an do:gs : : : and this is another test for dogs"
#tokens = get_primitive_tokens(line)
#freq_map = get_frequency_map(tokens)


# Calculating Frequency of Tokens
freq_map = frequency_from_file("testfile.txt")
# Sorting by Ascending Order
sorted_tuples = get_sorted_tuples(freq_map)
# Sorting by Descending Order (Reversing the list ....)
sorted_tuples.reverse()

print sorted_tuples

exit(0)
