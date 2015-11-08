import re, os, collections

SPLITTER = re.compile('[^\w]+')

def print_counter(path = 'shakespeare'):
    C = collections.Counter(all_words(path))
    print ('Total', sum(C.values()))
    print ('Distinct', len(C))
    return C

def each_work(path = 'shakespeare'):
    for root, dirs, files in os.walk(path):
        for work in files:
            yield (work, list(set(iterate_file(os.path.join(root, work)))))
    
def all_words(path = 'shakespeare'):
    for root, dirs, files in os.walk(path):
        for work in files:
            for word in iterate_file(os.path.join(root, work)):
                yield word

def distinct_words(path = 'shakespeare'):
    return list(set(all_words(path)))

def iterate_file(path):
    with open(path) as f:
        for line in f.readlines():
            for word in SPLITTER.split(line):
                if word:
                    yield word.lower()
        
        
