import shakespeare, sys, mmh3, math, collections, heapq, statistics
from collections import Counter

def percentile(N, percent, key=lambda x:x):
    """
    Find the percentile of a list of values.

    @parameter N - is a list of values. Note N MUST BE already sorted.
    @parameter percent - a float value from 0.0 to 1.0.
    @parameter key - optional key function to compute value from each element of N.

    @return - the percentile of the values
    """
    import math
    import functools

    if not N:
        return None
    k = (len(N)-1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return key(N[int(k)])
    d0 = key(N[int(f)]) * (c-k)
    d1 = key(N[int(c)]) * (k-f)
    return d0+d1


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

def real(works):
    real = {}
    for i in range(len(works)):
        for j in range(i+1, len(works)):
            name1, words1 = works[i]
            name2, words2 = works[j]
            real[(name1, name2)] = normal_compare(words1, words2)
    return real

if __name__ == '__main__':
    #shakespeare.write_duplicates()
    #sys.exit(0)

    works = list(shakespeare.each_work()) + list(shakespeare.each_work('duplicates'))

    real = real(works)
   
    hsig = minhash2_sig
    hcmp = minhash2

    hashes = {name: hsig(1000, A) for name, A in works}

    for k in range(25, 1001, 25):
        sys.stderr.write(str(k)+'\n')
        T = []
        for i in range(len(works)):
            for j in range(i+1, len(works)):
                name1, words1 = works[i]
                name2, words2 = works[j]
                normal = real[(name1, name2)]
                hashed = hcmp(k, hashes[name1][0:k], hashes[name2][0:k])
                T.append(abs(hashed-normal)/normal)
        T.sort()
        print('\t'.join(map(str, (k, statistics.mean(T), percentile(T, 0.90), percentile(T, 0.99)))))

