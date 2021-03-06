import re, os, collections, random, string

SPLITTER = re.compile('[^\w]+')

def print_counter(path = 'shakespeare'):
    C = collections.Counter(all_words(path))
    print ('Total', sum(C.values()))
    print ('Distinct', len(C))
    return C

def each_work(path = 'shakespeare'):
    for root, dirs, files in os.walk(path):
        for work in files:
            yield (os.path.join(root, work), list(set(iterate_file(os.path.join(root, work)))))

def each_work_raw(path = 'shakespeare'):
    for root, dirs, files in os.walk(path):
        for work in files:
            yield (os.path.join(root, work), list(iterate_file(os.path.join(root, work))))

    
def all_words(path = 'shakespeare'):
    for root, dirs, files in os.walk(path):
        for work in files:
            for word in iterate_file(os.path.join(root, work)):
                yield word

def write_duplicates(original = 'shakespeare', path = 'duplicates'):
    for root, dirs, files in os.walk(original):
        for work in files:
            original_words = list(iterate_file(os.path.join(root, work)))
            words = list(set(original_words))
            
            change = random.randint(0, len(words))
            for _ in range(change):
                index = random.randint(0, len(words)-1)
                words[index] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            
            print(work, len(original_words), len(words), change)
            os.makedirs(root.replace(original, path), exist_ok=True)
            with open(os.path.join(root.replace(original, path), work), mode='w') as f:
                f.write(' '.join(words))
    

def distinct_words(path = 'shakespeare'):
    return list(set(all_words(path)))

def iterate_file(path):
    with open(path) as f:
        for line in f.readlines():
            for word in SPLITTER.split(line):
                if word:
                    yield word.lower()
        
        
