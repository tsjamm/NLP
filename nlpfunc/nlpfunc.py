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

# This function returns the top n tuples in a freq map
def return_top_n_tuples(freq_map,n):
    total_uniques = 0;
    sorted_tuples = get_sorted_tuples(freq_map)
    sorted_tuples.reverse()
    to_return_tuples = []
    for pair in sorted_tuples:
        to_return_tuples.append(pair)
        total_uniques += 1
        if(total_uniques>=n):
            break
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
        self.pruned_clusters = {}
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
    
    def prune_clusters(self,max_num_per_cluster):
        for ci in self.clusters:
            self.pruned_clusters[ci] = []
            cluster_length = len(self.clusters[ci])
            if cluster_length <= max_num_per_cluster:
                self.pruned_clusters[ci] = self.clusters[ci]
                continue
            centroid = self.mu[ci]
            dist_map = {}
            for i in self.clusters[ci]:
                point = self.X[i]
                dist_map[i] = linalg.norm(point-centroid)
            top_max = return_top_n_tuples(dist_map, max_num_per_cluster)
            
            for pair in top_max:
                index = pair[0]
                self.pruned_clusters[ci].append(index);
            
# Basic Laplace Smoothing Maximum Likelihood Estimation
class BasicLaplaceSmoothing(object):
    
    def __init__(self,unigrams,ufreq,bfreq,tfreq):
        self.unigrams = unigrams
        self.uni_freq = ufreq
        self.bi_freq = bfreq
        self.tri_freq = tfreq
    
    #Calculates the individual probability of a trigram
    def calc_probability(self,trigram):
        # Add-One Smoothing
        numerator = 1.0
        # Adding V^3
        denominator = pow(len(self.uni_freq),3)
        
        tri = ' '.join(trigram)
        bi = ' '.join(trigram[0:2])
        
        if tri in self.tri_freq:
            # c(wi-2, wi-1, wi) + 1.0
            numerator += self.tri_freq[tri] 
        
        if bi in self.bi_freq:
            # c(wi-2, wi-1) + V
            denominator += self.bi_freq[bi] 
        
        probability = (numerator/denominator)
        return probability
    
    #Estimates the likelihood for a sentence
    def estimate_likelihood(self,trigrams):
        if len(trigrams) == 0:
            return 0.0
        probability = 1.0
        for trigram in trigrams:
            probability *= self.calc_probability(trigram)
        return probability

# Basic Good Turing Smoothing Maximum Likelihood Estimation
class BasicGoodTuringSmoothing(object):
    
    def __init__(self,unigrams,ufreq,bfreq,tfreq):
        self.unigrams = unigrams
        self.bins = {}
        self.unseen_probability = 0.0
        self.uni_freq = ufreq
        self.bi_freq = bfreq
        self.tri_freq = tfreq
        #Initializing Bins
        self.classify_bins()
    
    def classify_bins(self):
        for key in self.tri_freq:
            count = self.tri_freq[key]
            
            if count in self.bins:
                self.bins[count] += 1
            else:
                self.bins[count] = 1
        # N1/N, 0.0 for float
        self.unseen_probability = (self.bins[1] + 0.0) / (len(self.tri_freq)) 
    
    #Calculates the individual probability of a trigram
    def calc_probability(self,trigram):
        tri = ' '.join(trigram)
        
        if tri in self.tri_freq:
            c = self.tri_freq[tri]
            c_plus1 = c+1
            
            if c_plus1 in self.bins:
                # N sub c+1 exists
                nc_plus1 = self.bins[c_plus1]
                # N sub c 
                nc = self.bins[c] 
                
                # c* = (c+1) * Nc+1 / Nc
                c_star = (c_plus1 + 0.0) * nc_plus1 / nc
                # p(w) = c* / N
                probability = c_star / len(self.tri_freq)
                
                return probability
            else:
                # N sub c+1 = 0
                return self.unseen_probability 
        else:
            # trigram is unseen and new
            return self.unseen_probability        
        
        
        return probability
    
    #Estimates the likelihood for a sentence
    def estimate_likelihood(self,trigrams):
        if len(trigrams) == 0:
            return 0.0
        probability = 1.0
        for trigram in trigrams:
            probability *= self.calc_probability(trigram)
        return probability
    
# Linear Interpolation Back-Off Laplace Smoothing Maximum Likelihood Estimation
class IBOLaplaceSmoothing(object):
    
    def __init__(self,unigrams,ufreq,bfreq,tfreq):
        self.unigrams = unigrams
        self.total_count = len(unigrams)
        self.vocabulary = {}
        self.vocabulary[1] = ufreq
        self.vocabulary[2] = bfreq
        self.vocabulary[3] = tfreq
        self.unique_count = {}
        self.unique_count[1] = len(self.vocabulary[1]) # N for unigrams
        self.unique_count[2] = len(self.vocabulary[2]) # N for bigrams
        self.unique_count[3] = len(self.vocabulary[3]) # N for trigrams
        self.lambda_t = 0.5 #trigram Lambda
        self.lambda_b = 0.3 #bigram Lambda
        self.lambda_u = 0.2 #unigram Lambda
    
    #Calculates the individual probability of an ngram
    def calc_probability(self, ngram, n):
        # Add-One Smoothing
        numerator = 1.0
        # Adding V
        denominator = self.unique_count[1]
        
        # sequence used in numerator
        num_seq = ''
        # sequence used in denominator
        denom_seq = ''
        
        if n == 1:
            # use unigram
            num_seq = ngram[0]
            # N + V
            denominator += self.total_count
        else:
            # c(wi-n...wi)
            num_seq = ' '.join(ngram)
            
            if n == 2:
                # c(wi-1)
                denom_seq = ngram[0]
            else: # if n == 3:
                # c(wi-1,wi)
                denom_seq = ' '.join(ngram[0:2])
        
            if denom_seq in self.vocabulary[n-1]:
                # c(wi-2,wi-1) + V
                denominator += self.vocabulary[n-1][denom_seq]
        
        if num_seq in self.vocabulary[n]:
            # c(wi-n...wi) + 1.0 , to convert to float
            numerator += self.vocabulary[n][num_seq]
        
        probability = (numerator/denominator)
        return probability
    
    # Performs the Interpolation and returns probability
    def perform_interpolation(self,trigram):
        probability = 0.0
        probability += (self.lambda_t * self.calc_probability(trigram,3))
        probability += (self.lambda_b * self.calc_probability(trigram[-2:],2))
        probability += (self.lambda_u * self.calc_probability(trigram[-1:],1))
        return probability
    
    #Estimates the likelihood for a sentence
    def estimate_likelihood(self,trigrams):
        if len(trigrams) == 0:
            return 0.0
        probability = 1.0
        for trigram in trigrams:
            probability *= self.perform_interpolation(trigram)
        return probability
    
# Linear Interpolation Back-Off GoodTuring Smoothing Maximum Likelihood Estimation
class IBOGoodTuringSmoothing(object):
    
    def __init__(self,unigrams,ufreq,bfreq,tfreq):
        self.unigrams = unigrams
        self.bins = {}
        self.vocabulary = {}
        self.vocabulary[1] = ufreq
        self.vocabulary[2] = bfreq
        self.vocabulary[3] = tfreq
        self.unique_count = {}
        self.unique_count[1] = len(self.vocabulary[1]) # N for unigrams
        self.unique_count[2] = len(self.vocabulary[2]) # N for bigrams
        self.unique_count[3] = len(self.vocabulary[3]) # N for trigrams
        self.lambda_t = 0.5 #trigram Lambda
        self.lambda_b = 0.3 #bigram Lambda
        self.lambda_u = 0.2 #unigram Lambda
        #Classifying Bins
        self.classify_bins()
    
    def classify_bins(self):
        self.unseen_probability = {}
        
        for index in range(0,len(self.vocabulary)):
            ngram_order = index+1
            self.bins[ngram_order] = {} 
            
            for key in self.vocabulary[ngram_order]:
                count = self.vocabulary[ngram_order][key]
                
                if count in self.bins[ngram_order]:
                    self.bins[ngram_order][count] += 1
                else:
                    self.bins[ngram_order][count] = 1
            
            self.unseen_probability[ngram_order] = (self.bins[ngram_order][1] + 0.0) / (self.unique_count[ngram_order]) # N1/N , converting to float by adding 0.0
    
    
    #Calculates the individual probability of an ngram
    def calc_probability(self,ngram,n):
        sequence = ' '.join(ngram)
        
        if sequence in self.vocabulary[n]:
            c = self.vocabulary[n][sequence] # c
            cplus1 = c + 1 # c+1
            
            if cplus1 in self.bins[n]:
                ncplus1 = self.bins[n][cplus1] # N sub c+1 exists
                nc = self.bins[n][c] # N sub c
                
                cstar = (cplus1 + 0.0) * ncplus1 / nc # c* = (c+1) * Nc+1 / Nc
                probability = cstar / self.unique_count[n] # p(w) = c* / N
                
                return probability
            else:
                return self.unseen_probability[1] # N sub c+1 = 0
        else:
            return self.unseen_probability[1] # trigram is unseen and new
    
    # Performs the Interpolation and returns probability
    def perform_interpolation(self,trigram):
        probability = 0.0
        probability += (self.lambda_t * self.calc_probability(trigram,3))
        probability += (self.lambda_b * self.calc_probability(trigram[-2:],2))
        probability += (self.lambda_u * self.calc_probability(trigram[-1:],1))
        return probability
    
    #Estimates the likelihood for a sentence
    def estimate_likelihood(self,trigrams):
        if len(trigrams) == 0:
            return 0.0
        probability = 1.0
        for trigram in trigrams:
            probability *= self.perform_interpolation(trigram)
        return probability

#Viterbi PoS Tagging
class Viterbi(object):
    
    def __init__(self, input_params):
        self.states = input_params['states']
        self.observations = input_params['observations']
        self.start_probability = input_params['start_probability']
        self.transition_probability = input_params['transition_probability']
        self.emission_probability = input_params['emission_probability']
        #Executing Viterbi on the above parameters
        self.viterbi()

    def viterbi(self):
        obs = self.observations
        states = self.states
        start_p = self.start_probability
        trans_p = self.transition_probability
        emit_p = self.emission_probability
        
        V = [{}]
        path = {}
     
        # Initialize base cases (t == 0)
        for y in states:
            V[0][y] = start_p[y] * emit_p[y][obs[0]]
            path[y] = [y]
     
        # Run Viterbi for t > 0
        for t in range(1, len(obs)):
            V.append({})
            newpath = {}
     
            for y in states:
                (prob, state) = max((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)
                V[t][y] = prob
                newpath[y] = path[state] + [y]
     
            # Don't need to remember the old paths
            path = newpath
        # if only one element is observed max is sought in the initialization values
        n = 0
        if len(obs)!=1:
            n = t
        (prob, state) = max((V[n][y], y) for y in states)
        toReturnObj = (prob, path[state])
        print toReturnObj
        return toReturnObj