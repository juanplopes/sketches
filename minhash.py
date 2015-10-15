import shakespeare, sys, mmh3, math, collections, heapq

def normal_compare(A, B):
    SA = set(A)
    SB = set(B)
    return float(len(SA.intersection(SB))) / len(SA.union(SB))

def minhash1_sig(k, A):
    return [min(mmh3.hash(word, i) for word in A) for i in range(k)]

def minhash1(k, A, B):
    HA = minhash1_sig(k, A)
    HB = minhash1_sig(k, B)
    return sum(a==b for a, b in zip(HA, HB))/float(k)

def minhash2_sig(k, A):
    return heapq.nsmallest(k, (mmh3.hash(str(word), 0) for word in A))

def minhash2(k, A, B):
    HA = minhash2_sig(k, A)
    HB = minhash2_sig(k, B)
    HX = heapq.nsmallest(k, set(HA).union(HB))
    HY = set(HX).intersection(HA).intersection(HB)
    return len(HY)/float(k)


if __name__ == '__main__':
    works = list(shakespeare.each_work())
    
    for k in range(25, 2001, 25):
        sys.stderr.write(str(k)+'\n')
        T = [k]
        for i in range(len(works)):
            for j in range(i+1, len(works)):
                name1, words1 = works[i]
                name2, words2 = works[j]
                normal = normal_compare(words1, words2)
                mh1 = minhash2(k, words1, words2)
                T.append(mh1-normal)
        print '\t'.join(map(str, T))

