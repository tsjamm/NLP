#!/usr/bin/python

# Author: Sai Teja Jammalamadaka
# PGSSP Student : IIIT-Hyderabad
# Roll: 201350905
# Written for the Monsoon Semester 2014 NLP Course

# This is a primitive program that parses a given text into tokens
# Using Regular Expressions

import nlpfunc     #This is the custom written library of nlp functions

print "Runnning Program 1...."

# Sample line for testing
#line = "Cats are smarte's th-an do:gs : : : and this is another test for dogs"
#tokens = nlpfunc.get_primitive_tokens(line)
#tokens = nlpfunc.get_special_tokens(tokens)
#print tokens
#freq_map = nlpfunc.get_frequency_map(tokens)

# Calculating Frequency of Tokens
#freq_map = nlpfunc.frequency_from_file("testfile.txt")
#nlpfunc.write_to_file("testfile.processed.txt",freq_map)
#nlpfunc.process_file("testfile.txt")

# For Assignment
nlpfunc.process_file("../Datasets/English.txt")
nlpfunc.process_file("../Datasets/Hindi.txt")
nlpfunc.process_file("../Datasets/Telugu.txt")


exit(0)

