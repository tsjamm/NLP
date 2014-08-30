# just a dummy test file to test out code....
import re           # For Regex
from sys import argv

test_str = unicode(argv[1],"utf-8")

print test_str

punctuation_string = u'[].,<>/?!@#$%&*()~`\'\"\u0964\u0965;:+={}[|\^-]'
single_punct = re.compile(u'('+punctuation_string+')')

matches = re.findall(single_punct, test_str)

print matches

for m in matches:
    print m