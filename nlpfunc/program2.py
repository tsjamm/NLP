#!/usr/bin/python

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Monsoon Semester 2014 NLP Course

# program 2 - gets the 250 highest frequency words from a file,
# then constructs a co-occurrence matrix
# Then tries to apply k-means

import nlpfunc

from numpy import array

import os.path

print "Runnning Program 2...."

def process_file(file_path,file_name,n_tuples):
    freq_map = nlpfunc.get_frequency_map_from_file(file_path)
    tuple_list = nlpfunc.return_top_n_tuples(freq_map,n_tuples)
    del freq_map # Memory problems...
    
    # Need to construct co-occurrance matrix
    top_n_list = []
    top_n_map = {}
    top_n_index = 0
    for pair in tuple_list:
        token = pair[0]
        #for initializing empty dict in co-occurance mat
        top_n_map[token] = top_n_index
        top_n_list.append(0)
        top_n_index +=1
    
    print "Started Calculation of CoMatrix"
    
    modelleft = {}
    modelright = {}
    with open(file_path) as input_file:
        for input_line in input_file:
            input_tokens = nlpfunc.get_primitive_tokens(input_line)
            input_tokens = nlpfunc.get_special_tokens(input_tokens)
            input_tokens_length = len(input_tokens)
            if input_tokens_length<1:
                continue
            for x in range(0, input_tokens_length):
                token = input_tokens[x]
                if not token in modelleft:
                    modelleft[token] = list(top_n_list)
                if not token in modelright:
                    modelright[token] = list(top_n_list)
                
                if x==0 and x==input_tokens_length-1:
                    #do NO checks
                    continue
                elif x==0:
                    #do only right check
                    token_right = input_tokens[x+1]
                    if token_right in top_n_map:
                        modelright[token][top_n_map[token_right]] +=1
                elif x==input_tokens_length-1:
                    #do only left check
                    token_left = input_tokens[x-1]
                    if token_left in top_n_map:
                        modelleft[token][top_n_map[token_left]] +=1
                else:
                    #do both checks
                    token_right = input_tokens[x+1]
                    if token_right in top_n_map:
                        modelright[token][top_n_map[token_right]] +=1
                    token_left = input_tokens[x-1]
                    if token_left in top_n_map:
                        modelleft[token][top_n_map[token_left]] +=1
    
    #here model is the co-occurance matrix
    model = modelleft
    for key in modelright:
        if not key in model:
            model[key] = list(top_n_list)
        model[key].extend(modelright[key])
    
    print "Done Calculation CoMatrix"
    
    d = os.path.dirname(__file__) +"/../Results/A2/"+file_name+"/"
    if not os.path.exists(d):
        os.makedirs(d)
    with open(d+"Processed.comatrix_left."+file_name,'w') as output_file:
        output_file.write("{0}".format(modelleft))
    with open(d+"Processed.comatrix_right."+file_name,'w') as output_file:
        output_file.write("{0}".format(modelright))
    with open(d+"Processed.comatrix."+file_name,'w') as output_file:
        output_file.write("{0}".format(model))
    
    print "Done Writing to CoMatrix to files"
    
    model_keys = []
    model_points = []
    for key in model:
        model_keys.append(key)
        model_points.append(array(model[key]))
    
    kMeans = nlpfunc.KMeans()
    returned_tuple = kMeans.find_centers(model_points,50)
    print "mu is {0}".format(returned_tuple[0])
    print "number of clusters are {0}".format(len(returned_tuple[1]))



#For Assignment
#process_file("../Datasets/Toy_Data.txt", "ToyData",10)
process_file("../Datasets/Telugu.txt", "Telugu",250)

exit(0)

