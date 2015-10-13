import shakespeare, sys, mmh3, math, collections

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

if __name__ == '__main__':
    works = list(shakespeare.each_work())
    
    for k in range(25, 1001, 25):
        sys.stderr.write(str(k)+'\n')
        T = [k]
        for i in range(len(works)):
            for j in range(i+1, len(works)):
                name1, words1 = works[i]
                name2, words2 = works[j]
                normal = normal_compare(words1, words2)
                mh1 = minhash1(k, words1, words2)
                T.append(mh1-normal)
        print '\t'.join(map(str, T))

