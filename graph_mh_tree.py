import random, mmh3, collections, math, heapq, sys

def bitsoncount(i):
    assert 0 <= i < 0x100000000
    i = i - ((i >> 1) & 0x55555555)
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
    return (((i + (i >> 4) & 0xF0F0F0F) * 0x1010101) & 0xffffffff) >> 24

def gen_set(S, to):
    return [S[2*i+bitsoncount(i&to)%2] for i in xrange(len(S)/2)]

def unique_numbers():
    i = [0]
    def gen(n): 
        S = range(i[0], i[0]+n)
        i[0]+=n; 
        return S;
    return gen

def minhash_sig(A, k):
    return [min(mmh3.hash(str(word), i) for word in A) for i in xrange(k)]

def minhash(HA, HB, k):
    return sum(a==b for a, b in zip(HA, HB))/float(k)

def simhash_sig(A, k):
    n = 0
    for i in range(k):
        v = sum(1 if mmh3.hash(str(x), i)>0 else -1 for x in A)
        n = n*2+(v>=0)
    return n

def simhash(HA, HB, k):
    return (k-bin(HA^HB).count('1'))/float(k)

def random_tree(n, k, sim=True):
    N = unique_numbers()
    m = max(256, int(2**(math.ceil(math.log(n, 2))+1)))
    G = [(None, N(m))]

    for i in range(n-1):
        j = random.randint(0, i)
        _, S = G[j]
    
        G.append((j, gen_set(S, i) if len(S) == m else S+N(m/2)))
    return [(p, minhash_sig(S, k), simhash_sig(S, k) if sim else None, len(S) == m) for p, S in G]

def compute_error(G, k, delta1, delta2, sim=True):
    N = len(G)
    FN1, FN2, TN = 0, 0, 0
    FP1, FP2, TP = 0, 0, 0

    for i in range(N):
        for j in range(i+1, N):
            nei = G[i][0] == j or G[j][0] == i
            value1 = minhash(G[i][1], G[j][1], k)
            value2 = simhash(G[i][2], G[j][2], k) if sim else 0
            if not nei:
                if value1 >= delta1: FP1+=1
                if value2 >= delta2: FP2+=1
            else:
                if value1 <= delta1: FN1+=1
                if value2 <= delta2: FN2+=1

            if nei: TP += 1 
            else: TN += 1

    return (float(FP1)/TN, float(FN1)/TP, float(FP2)/TN, float(FN2)/TP)
    
def avg(L):
    return float(sum(L))/len(L)
    
def test_delta(N, k):
    X = 40
    RP1 = [[] for i in xrange(X+1)]
    RN1 = [[] for i in xrange(X+1)]
    RP2 = [[] for i in xrange(X+1)]
    RN2 = [[] for i in xrange(X+1)]

    for test in range(100):
        sys.stderr.write(str(test)+'\n')
        G = random_tree(N, k)
        for delta in range(X+1):
            FP1, FN1, FP2, FN2 = compute_error(G, k, delta/float(X), delta/float(X))
            RP1[delta].append(FP1)
            RN1[delta].append(FN1)
            RP2[delta].append(FP2)
            RN2[delta].append(FN2)
            
    for delta in range(0, X+1):
        print '\t'.join(str(x) for x in (delta/float(X), avg(RP1[delta]), avg(RN1[delta]), avg(RP2[delta]), avg(RN2[delta])))

def test_size(k):
    X = 20
    RP1 = [[] for i in xrange(X+1)]
    RN1 = [[] for i in xrange(X+1)]
    RP2 = [[] for i in xrange(X+1)]
    RN2 = [[] for i in xrange(X+1)]

    for test in range(100):
        for delta in range(1, X+1):
            sys.stderr.write(str(test)+' '+str(delta)+'\n')    
            N = int(delta/float(X)*200)
            G = random_tree(N, k, False)
            FP1, FN1, FP2, FN2 = compute_error(G, k, 0.375, 0.671173911, False)
            RP1[delta].append(FP1)
            RN1[delta].append(FN1)
            RP2[delta].append(FP2)
            RN2[delta].append(FN2)
            
    for delta in range(1, X+1):
        N = int(delta/float(X)*200)
        print '\t'.join(str(x) for x in (N, avg(RP1[delta]), avg(RN1[delta]), avg(RP2[delta]), avg(RN2[delta])))

def test_k():
    X = 8
    RP1 = [[] for i in xrange(X+1)]
    RN1 = [[] for i in xrange(X+1)]
    RP2 = [[] for i in xrange(X+1)]
    RN2 = [[] for i in xrange(X+1)]

    for test in range(100):
        for delta in range(1, X+1):
            sys.stderr.write(str(test)+' '+str(delta)+'\n')    
            N = 200
            k = int(delta/float(X)*128)
            G = random_tree(N, k, False)
            FP1, FN1, FP2, FN2 = compute_error(G, k, 0.375, 0.671173911, False)
            RP1[delta].append(FP1)
            RN1[delta].append(FN1)
            RP2[delta].append(FP2)
            RN2[delta].append(FN2)
            
    for delta in range(1, X+1):
        N = int(delta/float(X)*128)
        print '\t'.join(str(x) for x in (N, avg(RP1[delta]), avg(RN1[delta]), avg(RP2[delta]), avg(RN2[delta])))


#test_delta(25, 128)
test_size(128)
#test_k()
