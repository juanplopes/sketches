import shakespeare, sys, mmh3, math, collections, heapq, statistics
from collections import Counter

def normal_compare(A, B):
    SA = set(A)
    SB = set(B)
    return float(len(SA.intersection(SB))) / len(SA.union(SB))

def minhash1_sig(k, A):
    return [min(mmh3.hash(word, i) for word in A) for i in range(k)]

def minhash1(k, HA, HB):
    return sum(a==b for a, b in zip(HA, HB))/float(k)

def minhash2_sig(k, A):
    return heapq.nsmallest(k, (mmh3.hash(str(word), 0) for word in A))

def minhash2(k, HA, HB):
    HX = heapq.nsmallest(k, set(HA).union(HB))
    HY = set(HX).intersection(HA).intersection(HB)
    return len(HY)/float(k)

if __name__ == '__main__':
    hsig = minhash1_sig
    hcmp = minhash1

    works = list(shakespeare.each_work())

    hashes = {name: hsig(1000, A) for name, A in works}

    real = {}
    for i in range(len(works)):
        for j in range(i+1, len(works)):
            name1, words1 = works[i]
            name2, words2 = works[j]
            real[(name1, name2)] = normal_compare(words1, words2)

    for k in range(25, 1001, 25):
        sys.stderr.write(str(k)+'\n')
        T = []
        for i in range(len(works)):
            for j in range(i+1, len(works)):
                name1, words1 = works[i]
                name2, words2 = works[j]
                normal = real[(name1, name2)]
                hashed = hcmp(k, hashes[name1][0:k], hashes[name2][0:k])
                T.append(hashed-normal)
        print('\t'.join(map(str, (k, statistics.mean(T), min(T), max(T), statistics.stdev(T),-statistics.stdev(T)))))

