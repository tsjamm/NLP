#!/usr/bin/python

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Monsoon Semester 2014 NLP Course

# program 4 - Viterbi PoS Tagging

import time
#import os.path

print "Runnning Program 4...."
starttime = time.asctime( time.localtime(time.time()) )
print "Start Time :", starttime

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
        self.print_dptable(V)
        (prob, state) = max((V[n][y], y) for y in states)
        toReturnObj = (prob, path[state])
        print toReturnObj
        return toReturnObj

    # Don't study this, it just prints a table of the steps.
    def print_dptable(self, V):
        s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
        for y in V[0]:
            s += "%.8s: " % y
            s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
            s += "\n"
        print(s)




#Example Input Parameters for Viterbi algorithm
input_params = {}
input_params['states'] = ('Healthy', 'Fever')
input_params['observations'] = ('normal', 'cold', 'dizzy')
input_params['start_probability'] = {'Healthy': 0.6, 'Fever': 0.4}
input_params['transition_probability'] = {'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},'Fever' : {'Healthy': 0.4, 'Fever': 0.6}}
input_params['emission_probability'] = {'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}}
#Running Viterbi on the above example parameters
vit = Viterbi(input_params)
        
#For Assignment


endtime = time.asctime( time.localtime(time.time()) )
print "Start Time :", starttime
print "End Time :", endtime

exit(0)
