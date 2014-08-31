#!/usr/bin/python

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Monsoon Semester 2014 NLP Course


# This is a primitive program that contains miscellaneous functions
# for tokenization using regular expressions,
# calculating freq maps,
# clustering with k-means,
# smoothing,
# etc.


import re           # For Regex
import operator     # For Ordering by Value

import random
from numpy import linalg
from numpy import mean

# To Extract non-space charactered tokens (primitive tokens)
primitive_token_detection = re.compile(u'[^\s]+')

# This function returns the primitive non space tokens
# in the given input string
def get_primitive_tokens(text):
    #text_unicode = unicode(text,"utf-8")
    list_obj = re.findall(primitive_token_detection,text)
    if list_obj:
        return list_obj
    else:
        return []

# non-word character at start or end of token (lower pref compared to above regexps)
punctuation_string = u'[].,<>/?!@#$%&*()~`\'\"\u0964\u0965\u2018;:+={}[|\^-]'
punctuation = re.compile(u'^'+punctuation_string+'+|'+punctuation_string+'+$') 
punctuation_start = re.compile(u'^'+punctuation_string+'+') 
punctuation_end = re.compile(u''+punctuation_string+'+$') 

# detecting punctuation anywhere...
single_punct = re.compile(u'('+punctuation_string+')')

# To Extract special tokens like . , ? / and so on...
initials = re.compile(u'^[\w]\.(\w\.)*',re.U)               # S.P.   or for U.S.A. or e.g.
titles = re.compile(u'[A-Z]+[a-z]*\.')                      # Dr. Mr. Prof.
quote_s = re.compile(u'[^\s]+\'s')                          # King's
hyphenation = re.compile(u"\w+-\w+(-\w+)*")                 # state-of-the-art
numbers = re.compile(u"\d+|\d+[:.]\d+(\.\d+)*\w*|\d+\w*")   # 4, 3:15, 192.168.2.1, 9.8ms, 34th
dates = re.compile(u"\d+[.-/]\d+[.-/]\d+")                  # 21-12-14, 7-12-2020, 3.03.43
url = re.compile(u"^http://|^https://|^ftp://|^file:///")   # urls starting with these

# This function checks certain special tokens like punctuation marks and so on
def get_special_tokens(token_list):
    special_tokens = []
    for token in token_list:
        #token = unicode(raw_token,"utf-8")
        special_tokens_in_token = []
        punctuation_obj = re.findall(single_punct,token)    #First check if it contains punctuation
        #print "punctuation_obj = ",punctuation_obj," token = "+token
        
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
                        special_tokens_in_token.extend(single_punct_obj)
                    else:
                        special_tokens_in_token.append(punct_token)
                        
                center_token = re.sub(punctuation, "", token)
                quote_s_obj = re.findall(quote_s,center_token)
                hyphen_obj = re.findall(hyphenation,center_token)
                number_obj = re.findall(numbers,center_token)
                date_obj = re.findall(dates,center_token)
                token_split_obj = re.split(single_punct, center_token)
                if (not quote_s_obj) and (not hyphen_obj) and (not number_obj) and (not date_obj) and (token_split_obj):
                    special_tokens_in_token.extend(token_split_obj)
                else:
                    special_tokens_in_token.append(center_token)
                
                for punct_token in punct_end_obj:
                    single_punct_obj = re.findall(single_punct, punct_token)
                    if single_punct_obj:
                        special_tokens_in_token.extend(single_punct_obj)
                    else:
                        special_tokens_in_token.append(punct_token)
                
        if (not punctuation_obj):
            special_tokens.append(token)
    to_return = []
    for st in special_tokens:
        if st != "" and st!=" ":
            to_return.append(st)
    return to_return
            

# This function returns a list of sorted tuples from the input frequency map
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
def write_freq_map_to_file(file_path,freq_map):
    total_freq = 0;
    total_uniques = 0;
    sorted_tuples = get_sorted_tuples(freq_map)
    sorted_tuples.reverse()
    with open(file_path,'w') as output_file:
        for pair in sorted_tuples:
            output_file.write("{0}\t{1}\n".format(pair[0].encode("utf-8"),pair[1]))
            total_freq += pair[1]
            total_uniques += 1
        #output_file.write("Total Number of Tokens : {0}\n".format(total_freq))
        #output_file.write("Total Number of Uniques : {0}\n".format(total_uniques))
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

# This function takes the top n entries in freq map and writes to file
def write_top_n_to_file(file_path,freq_map, top_n):
    top_n_tuples = return_top_n_tuples(freq_map,top_n)
    with open(file_path,'w') as output_file:
        for pair in top_n_tuples:
            output_file.write("{0}\t{1}\n".format(pair[0].encode("utf-8"),pair[1]))
    print "Finished writing to File : "+file_path

# This function returns the top n unique tokens
def return_top_n_tuples(freq_map,n):
    total_freq = 0;
    total_uniques = 0;
    sorted_tuples = get_sorted_tuples(freq_map)
    sorted_tuples.reverse()
    to_return_tuples = []
    for pair in sorted_tuples:
        to_return_tuples.append(pair)
        total_freq += pair[1]
        total_uniques += 1
        if(total_uniques>=n):
            break
    print "Total Number of Tokens : {0}".format(total_freq)
    print "Returning Top {0}\n".format(total_uniques)
    return to_return_tuples

# This function takes the last n entries in freq map and writes to file
def write_last_n_to_file(file_path,freq_map, last_n):
    last_n_tuples = return_last_n_tuples(freq_map, last_n)
    with open(file_path,'w') as output_file:
        for pair in last_n_tuples:
            output_file.write("{0}\t{1}\n".format(pair[0].encode("utf-8"),pair[1]))
    print "Finished writing to File : "+file_path

# This function returns the top n unique tokens
def return_last_n_tuples(freq_map,n):
    total_freq = 0;
    total_uniques = 0;
    sorted_tuples = get_sorted_tuples(freq_map)
    sorted_tuples.reverse()
    to_return_tuples = []
    length = len(sorted_tuples);
    for pair in sorted_tuples:
        if(total_uniques>length-n):
            to_return_tuples.append(pair)
            total_freq += pair[1]
        total_uniques += 1
    print "Total Number of Tokens : {0}".format(total_freq)
    print "Returning Last {0}\n".format(total_uniques)
    return to_return_tuples

# This function takes the middle n unique tokens and writes to file
def write_middle_n_to_file(file_path,freq_map, middle_n):
    middle_n_tuples = return_middle_n_tuples(freq_map, middle_n)
    with open(file_path,'w') as output_file:
        for pair in middle_n_tuples:
            output_file.write("{0}\t{1}\n".format(pair[0].encode("utf-8"),pair[1]))
    print "Finished writing to File : "+file_path

# This function returns the top n unique tokens
def return_middle_n_tuples(freq_map,n):
    total_freq = 0;
    total_uniques = 0;
    sorted_tuples = get_sorted_tuples(freq_map)
    sorted_tuples.reverse()
    to_return_tuples = []
    length = len(sorted_tuples);
    middle_length = length/2;
    middle_start = middle_length-(n/2)
    middle_end = middle_length+(n/2)
    for pair in sorted_tuples:
        if (total_uniques>middle_start) and (total_uniques< middle_end):
            to_return_tuples.append(pair)
            total_freq += pair[1]
        if (total_uniques>=middle_end):
            break;
        total_uniques += 1
    print "Total Number of Tokens : {0}".format(total_freq)
    print "Returning Middle {0}\n".format(len(to_return_tuples))
    return to_return_tuples

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
            output_file.write(line.encode("utf-8")+"\n")
            total_count += 1
        #output_file.write("Total Number of Tokens : {0}\n".format(total_count))
    print "Finished writing to File : "+file_path
    print "Total Number of Tokens : {0}\n".format(total_count)

# This function writes a tuples list to file
def write_tuples_to_file(file_path,tuple_list):
    total_freq = 0;
    total_uniques = 0;
    with open(file_path,'w') as output_file:
        for pair in tuple_list:
            output_file.write("{0}\t{1}\n".format(pair[0].encode("utf-8"),pair[1]))
            total_freq += pair[1]
            total_uniques += 1
    print "Finished writing to File : "+file_path
    print "Total Number of Tokens : {0}".format(total_freq)
    print "Total Number of Uniques : {0}\n".format(total_uniques)
    
    
# This function reads a given file line by line and processes the tokenization
def get_frequency_map_from_file(file_path):
    freq_map = {}
    total_freq = 0;
    with open(file_path) as input_file:
        for input_line in input_file:
            input_tokens = get_primitive_tokens(input_line)
            input_tokens = get_special_tokens(input_tokens)
            total_freq += len(input_tokens)
            freq_map = get_frequency_map(input_tokens,freq_map)
    total_uniques = len(freq_map)
    print "Total Uniques : {0}".format(total_uniques)
    print "Total Number of Tokens : {0}".format(total_freq)
    return freq_map

# This function reads a given file line by line and processes the tokenization
# and returns the ngram frequency map
def get_ngram_frequency_map_from_file(file_path,ngram):
    freq_map = {}
    total_freq = 0;
    with open(file_path) as input_file:
        for input_line in input_file:
            input_tokens = get_primitive_tokens(input_line)
            input_tokens = get_special_tokens(input_tokens)
            input_ngrams = get_n_grams(ngram, input_tokens)
            total_freq += len(input_ngrams)
            freq_map = get_frequency_map(input_ngrams,freq_map)
    total_uniques = len(freq_map)
    print "Total Uniques : {0}".format(total_uniques)
    print "Total Number of "+str(ngram)+"-Ngrams : {0}".format(total_freq)
    return freq_map


# K-Means clustering
class KMeans(object):
    
    def __init__(self, X, K):
        self.X = X
        self.K = K
        # Initialize to K random centers
        self.mu = random.sample(X, K)
        self.oldmu = random.sample(X, K)
        self.clusters = {}
        self.iterations = 0;
        self.zero_iterations = 0;
        #Invoking the KMeans
        self.find_centers()

    def find_centers(self):
        while not self.has_converged():
            print "This is iteration {0}".format(self.iterations)
            self.oldmu = self.mu
            # Assign all points in X to clusters
            self.cluster_points()
            # Reevaluate centers
            self.reevaluate_centers()
            # Making sure there are no zero clusters...
            while len(self.mu) < self.K :
                for mi, m in enumerate(self.oldmu):
                    try:
                        self.clusters[mi]
                    except KeyError:
                        self.mu.append(random.sample(self.X, 1)[0])
                self.cluster_points();
                self.zero_iterations+=1
            
            print "Zero Cluster Removal iterations = {0}".format(self.zero_iterations)
            
            self.iterations+=1
        print "Has Converged....."
    
    def cluster_points(self):
        X = self.X
        mu = self.mu
        clusters  = {}
        for xi in range(0,len(X)):
            x=X[xi];
            bestmukey = min([(i[0], linalg.norm(x-mu[i[0]])) for i in enumerate(mu)], key=lambda t:t[1])[0]
            try:
                clusters[bestmukey].append(xi)
            except KeyError:
                clusters[bestmukey] = [xi]            
        self.clusters = clusters
    
    def reevaluate_centers(self):
        newmu = []
        keys = sorted(self.clusters.keys())
        for k in keys:
            cluster_points = []
            for index in self.clusters[k]:
                cluster_points.append(self.X[index])
            newmu.append(mean(cluster_points, axis = 0))
        self.mu = newmu
    
    def has_converged(self):
        toReturn = (set([tuple(a.tolist()) for a in self.mu]) == set([tuple(a.tolist()) for a in self.oldmu]))
        return toReturn