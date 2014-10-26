#!/usr/bin/python

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Monsoon Semester 2014 NLP Course

# program 4 - Viterbi PoS Tagging

import nlpfunc
import time
#import os.path

print "Runnning Program 4...."
starttime = time.asctime( time.localtime(time.time()) )
print "Start Time :", starttime

#The class for this program goes here......


#Example Input Parameters for Viterbi algorithm
input_params = {}
input_params['states'] = ('Healthy', 'Fever')
input_params['observations'] = ('normal', 'cold', 'dizzy')
input_params['start_probability'] = {'Healthy': 0.6, 'Fever': 0.4}
input_params['transition_probability'] = {'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},'Fever' : {'Healthy': 0.4, 'Fever': 0.6}}
input_params['emission_probability'] = {'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}}
#Running Viterbi on the above example parameters
vit = nlpfunc.Viterbi(input_params)
        
#For Assignment


endtime = time.asctime( time.localtime(time.time()) )
print "Start Time :", starttime
print "End Time :", endtime

exit(0)
