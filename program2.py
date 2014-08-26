#!/usr/bin/python

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Monsoon Semester 2014 NLP Course

# program 2 - gets the 250 highest frequency words from a file,
# then constructs a co-occurrence matrix

import nlpfunc      # Custom Written Functions for this course

import numpy as np
import random


freq_map = nlpfunc.get_frequency_map_from_file('English.txt')
#bigram_freq_map = nlpfunc.get_bigram_frequency_map_from_file('English.txt')
tuple_list = nlpfunc.return_top_n_tuples(freq_map,250)
del freq_map # Memory problems...
#nlpfunc.write_tuples_to_file('Processed.top250.English.txt',tuple_list)

# Need to construct co-occurrance matrix using the bigram_freq_map
top250list = []
top250map = {}
top250index = 0
for pair in tuple_list:
    token = pair[0]
    #top250list.append(token)
    #for initializing empty dict in co-occurance mat
    top250map[token] = top250index
    top250list.append(0)
    top250index +=1


#top250bigrams = nlpfunc.get_n_grams(2, top250list)
#for bigram in top250bigrams:
#    if bigram in bigram_freq_map:
#       print "bigram exists with freq={0} ::: {1}".format(bigram_freq_map[bigram],bigram)

print "Started Calculation of CoMatrix"

modelleft = {}
modelright = {}
with open('English.txt') as input_file:
    for input_line in input_file:
        input_tokens = nlpfunc.get_primitive_tokens(input_line)
        input_tokens = nlpfunc.get_special_tokens(input_tokens)
        input_tokens_length = len(input_tokens)
        if input_tokens_length<1:
            continue
        for x in range(0, input_tokens_length):
            token = input_tokens[x]
            if not token in modelleft:
                modelleft[token] = list(top250list)
            if not token in modelright:
                modelright[token] = list(top250list)
            
            if x==0 and x==input_tokens_length-1:
                #do NO checks
                continue
            elif x==0:
                #do only right check
                token_right = input_tokens[x+1]
                if token_right in top250map:
                    modelright[token][top250map[token_right]] +=1
            elif x==input_tokens_length-1:
                #do only left check
                token_left = input_tokens[x-1]
                if token_left in top250map:
                    modelleft[token][top250map[token_left]] +=1
            else:
                #do both checks
                token_right = input_tokens[x+1]
                if token_right in top250map:
                    modelright[token][top250map[token_right]] +=1
                token_left = input_tokens[x-1]
                if token_left in top250map:
                    modelleft[token][top250map[token_left]] +=1

print "Done Calculation CoMatrix"

with open('Processed.comatrix_left.English.txt','w') as output_file:
    output_file.write("{0}".format(modelleft))
with open('Processed.comatrix_right.English.txt','w') as output_file:
    output_file.write("{0}".format(modelright))

print "Done Writing to comat to files"


def find_centers(X, K):
    # Initialize to K random centers
    oldmu = random.sample(X, K)
    mu = random.sample(X, K)
    while not has_converged(mu, oldmu):
        oldmu = mu
        clusters = cluster_points(X, mu) # Assign all points in X to clusters
        mu = reevaluate_centers(oldmu, clusters) # Reevaluate centers
    return(mu, clusters)

def cluster_points(X, mu):
    clusters  = {}
    for x in X:
        #for xi in enumerate(mu):
        #    print x
        #    print xi
        #    print xi[0]
        #    print mu[xi[0]]
        #    print np.linalg.norm(x-mu[xi[0]])
        bestmukey = min([(i[0], np.linalg.norm(x-mu[i[0]])) \
                    for i in enumerate(mu)], \
                    key=lambda t:t[1])[0]
        #print bestmukey
        try:
            clusters[bestmukey].append(x)
        except KeyError:
            clusters[bestmukey] = [x]
    return clusters

def reevaluate_centers(mu, clusters):
    newmu = []
    keys = sorted(clusters.keys())
    for k in keys:
        newmu.append(np.mean(clusters[k], axis = 0))
    return newmu

def has_converged(mu, oldmu):
    toReturn = (set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]))
    return toReturn

model = modelleft
for key in modelright:
    if not key in model:
        model[key] = list(top250list)
    model[key].extend(modelright[key])

model_keys = []
model_points = []
for key in model:
    #print key
    model_keys.append(key)
    #print model[key]
    model_points.append(np.array(model[key]))

returned_tuple = find_centers(model_points,50)
print "mu is {0}".format(returned_tuple[0])
print "number of clusters are {0}".format(len(returned_tuple[1]))

exit(0)

