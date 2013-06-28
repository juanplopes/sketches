import re, os

SPLITTER = re.compile('[^\w]+')

def all_words(path = 'shakespeare'):
    for root, dirs, files in os.walk(path):
        for work in files:
            for word in iterate_file(os.path.join(root, work)):
                yield word

def iterate_file(path):
    with open(path) as f:
        for line in f.readlines():
            for word in SPLITTER.split(line):
                if word:
                    yield word.lower()
        
        
