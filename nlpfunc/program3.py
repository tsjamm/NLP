#!/usr/bin/python

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Monsoon Semester 2014 NLP Course

# program 3 - Language Modeling and Smoothing 

import nlpfunc
import time
import os.path

print "Runnning Program 3...."
starttime = time.asctime( time.localtime(time.time()) )
print "Start Time :", starttime

class LanguageModelSmoothing(object):
    
    def __init__(self, training_file, test_file, output_name):
        self.training_file = training_file
        self.test_file = test_file
        self.output_name = output_name
        self.freq_map = {}
        self.unigrams = []
        self.freq_map_b = {}
        self.bigrams = []
        self.freq_map_t = {}
        self.trigrams = []
        #Loading the Frequencies
        self.populate_frequency_data()
        #Executing Likelihood Calculation on Test Data
        self.execute_on_test_file()
        
    def populate_frequency_data(self):
        with open(self.training_file) as input_file:
            for input_line_raw in input_file:
                input_line = unicode(input_line_raw,"utf-8")
                #Getting Unigrams
                input_tokens = nlpfunc.get_primitive_tokens(input_line)
                input_tokens = nlpfunc.get_special_tokens(input_tokens)
                self.unigrams.extend(input_tokens)
                self.freq_map = nlpfunc.get_frequency_map(input_tokens,self.freq_map)
                #Getting Bigrams
                input_bigrams = nlpfunc.get_n_grams(2, input_tokens)
                self.bigrams.extend(input_bigrams)
                self.freq_map_b = nlpfunc.get_frequency_map(input_bigrams,self.freq_map_b)
                #Getting Trigrams
                input_trigrams = nlpfunc.get_n_grams(3, input_tokens)
                self.trigrams.extend(input_trigrams)
                self.freq_map_t = nlpfunc.get_frequency_map(input_trigrams,self.freq_map_t)

    def execute_on_test_file(self):
        d = os.path.dirname(__file__) +"../results/A3/"+self.output_name+"/"
        if not os.path.exists(d):
            os.makedirs(d)
       
        basicLS = nlpfunc.BasicLaplaceSmoothing(self.unigrams, self.freq_map,self.freq_map_b,self.freq_map_t)
        bLS_output = open(d+"BasicLaplaceSmoothing."+self.output_name,'w')
        
        basicGT = nlpfunc.BasicGoodTuringSmoothing(self.unigrams, self.freq_map,self.freq_map_b,self.freq_map_t)
        bGT_output = open(d+"BasicGoodTuringSmoothing."+self.output_name,'w')
        
        iboLS = nlpfunc.IBOLaplaceSmoothing(self.unigrams, self.freq_map,self.freq_map_b,self.freq_map_t)
        iboLS_output = open(d+"IBOLaplaceSmoothing."+self.output_name,'w')
        
        iboGT = nlpfunc.IBOGoodTuringSmoothing(self.unigrams, self.freq_map,self.freq_map_b,self.freq_map_t)
        iboGT_output = open(d+"IBOGoodTuringSmoothing."+self.output_name,'w')
        
        smoothing_output = open(d+"Smoothing."+self.output_name,'w')
        
        with open(self.test_file) as input_file:
            for input_line_raw in input_file:
                input_line = unicode(input_line_raw,"utf-8")
                #Reading Tokens
                input_tokens = nlpfunc.get_primitive_tokens(input_line)
                input_tokens = nlpfunc.get_special_tokens(input_tokens)
                #Getting Trigrams
                input_trigrams = nlpfunc.get_n_grams(3, input_tokens)
                
                #Calucalting Likelihoods
                bls_likelihood = basicLS.estimate_likelihood(input_trigrams)
                bLS_output.write(str(bls_likelihood)+" is BLS-MLE of "+input_line_raw)
                bgt_likelihood = basicGT.estimate_likelihood(input_trigrams)
                bGT_output.write(str(bgt_likelihood)+" is BGT-MLE of "+input_line_raw)
                ibols_likelihood = iboLS.estimate_likelihood(input_trigrams)
                iboLS_output.write(str(ibols_likelihood)+" is IBOLS-MLE of "+input_line_raw)
                ibogt_likelihood = iboGT.estimate_likelihood(input_trigrams)
                iboGT_output.write(str(ibogt_likelihood)+" is IBOGT-MLE of "+input_line_raw)
                
                toCompare = {}
                toCompare['bls'] = bls_likelihood
                toCompare['bgt'] = bgt_likelihood
                toCompare['ibols'] = ibols_likelihood
                toCompare['ibogt'] = ibogt_likelihood
                sorted_tuples = nlpfunc.get_sorted_tuples(toCompare)
                sorted_tuples.reverse()
                smoothing_output.write(str(sorted_tuples))
                smoothing_output.write("\n")
                smoothing_output.write(input_line_raw)
                smoothing_output.write("\n")
                print sorted_tuples
                print input_line_raw
                
                        
        bLS_output.close()
        bGT_output.close()
        iboLS_output.close()
        iboGT_output.close()
        smoothing_output.close()

#For Assignment
# First Parameter is Training Data, Second is Test Data, Third is output name
#langModel = LanguageModelSmoothing("../datasets/Toy_Data.txt","../test-data/English.txt","ToyData")
#langModel = LanguageModelSmoothing("../datasets/English.txt","../test-data/English.txt","English")
#langModel = LanguageModelSmoothing("../datasets/Hindi.txt","../test-data/Hindi.txt","Hindi")
#langModel = LanguageModelSmoothing("../datasets/Telugu.txt","../test-data/Telugu.txt","Telugu")
langModel = LanguageModelSmoothing("../datasets/Telugu.txt","../evalutionData/Telugu_UTF.txt","TeluguEvaluation")


endtime = time.asctime( time.localtime(time.time()) )
print "Start Time :", starttime
print "End Time :", endtime

exit(0)