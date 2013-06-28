from shakespeare import all_words
from sys import stdin
from mmh3 import hash as mmhash

class Bloom:
    def __init__(self, n, hashes):
        self.data = [0] * n
        self.hashes = hashes
        
    def add(self, word):
        for i in range(self.hashes):
            self.data[mmhash(word, i) % len(self.data)] = 1

    def contains(self, word):
        return all(self.data[mmhash(word, i) % len(self.data)] for i in range(self.hashes))


S = set()
B = Bloom(2**15, 1)
c = 0
for word in all_words():
    c += 1
    S.add(word)
    B.add(word)
    
print 'Loaded ', c, len(S)
for test in iter(stdin.readline, ''):
    test = test.strip().lower()
    
    print 'Bloom filter: ', B.contains(test)
    print 'Set: ', test in S
            
            
