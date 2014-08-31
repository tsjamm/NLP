# just a dummy test file to test out code....
import re           # For Regex
from sys import argv
from array import array

test_str = unicode(argv[1],"utf-8")

print test_str

punctuation_string = u'[].,<>/?!@#$%&*()~`\'\"\u0964\u0965;:+={}[|\^-]'
single_punct = re.compile(u'('+punctuation_string+')')

matches = re.findall(single_punct, test_str)

print matches

for m in matches:
    print m
    
    
import numpy as np
mu = [[1.0],[1.0,2.3],[3.2],[4],[5]]
oldmu = [[1.0,2.3],[1.0],[3.2],[4],[5]]
toReturn = (set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]))

print toReturn

mu = []
oldmu = []
mu.append(np.array([1.0]))
mu.append(np.array([1.0,2.3]))
mu.append(np.array([3.0]))
mu.append(np.array([4.0]))
mu.append(np.array([5.2]))
print mu
oldmu.append(np.array([1.0]))
oldmu.append(np.array([1.0,2.3]))
oldmu.append(np.array([3.0]))
oldmu.append(np.array([4.0]))
oldmu.append(np.array([5.2]))
print oldmu

print set([tuple(a) for a in mu])
print set([tuple(a) for a in oldmu])

toReturn = (set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]))

print toReturn