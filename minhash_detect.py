import shakespeare, sys, mmh3, math, collections, heapq, statistics
from collections import Counter

def normal_compare(A, B):
    SA = set(A)
    SB = set(B)
    return float(len(SA.intersection(SB))) / len(SA.union(SB))

def minhash1_sig(k, A):
    return [min(mmh3.hash(word, i) for word in A) for i in range(k)]

def clusters(hashes, r, b):
    pairs = set()
    for i in range(b):
        C = collections.defaultdict(lambda: [])
        for name, sig in hashes.items():
            old = C[tuple(sig[r*i:r*i+r])]
            for other in old:
                pairs.add(frozenset((name, other)))
            old.append(name)
    return pairs

def prob(b, r, p):
    return (1 - (1-p)**(1/b))**(1/r)
        
if __name__ == '__main__':
"""
    for logb in range(1, 10):
        b = 2**logb
        r = 512/b
        su = prob(b, r, 0.995)
        sl = prob(b, r, 0.005)
        print(b, su, sl)
"""
    hsig = minhash1_sig

    works = list(shakespeare.each_work()) + list(shakespeare.each_work('duplicates'))
    works_dic = dict(works)

    hashes = {name: hsig(512, A) for name, A in works}

    real = {}
    for i in range(len(works)):
        for j in range(i+1, len(works)):
            name1, words1 = works[i]
            name2, words2 = works[j]
            real[frozenset((name1, name2))] = normal_compare(words1, words2)

    for logb in range(1, 9):
        b = 2**logb
        r = 512/b
        su = prob(b, r, 0.99)
        sl = prob(b, r, 0.01)
        
        pairs = clusters(hashes, int(r), int(b))

        for x, y in pairs:
            print(b, normal_compare(works_dic[x], works_dic[y]))
        
        #print(r, b, sl, su, len(pairs), len(expectedU-pairs), len(pairs-expectedL))
   
